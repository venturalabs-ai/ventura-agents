export type DomainEvent<T = unknown> = Readonly<{ id: string; type: string; occurredAt: string; payload: T }>;
export type EventHandler<T = unknown> = (event: DomainEvent<T>) => void | Promise<void>;
export class EventBus {
  private readonly handlers = new Map<string, Set<EventHandler>>();
  private readonly processed = new Set<string>();
  subscribe<T>(type: string, handler: EventHandler<T>): () => void {
    const handlers = this.handlers.get(type) ?? new Set<EventHandler>();
    handlers.add(handler as EventHandler); this.handlers.set(type, handlers);
    return () => handlers.delete(handler as EventHandler);
  }
  async publish<T>(event: DomainEvent<T>): Promise<boolean> {
    if (this.processed.has(event.id)) return false;
    this.processed.add(event.id);

    // ⚡ Bolt Optimization: Iterate directly over the Set instead of spreading to an array.
    // Also letting TS infer the array type to safely capture returned Handler results.
    const promises = [];
    const handlers = this.handlers.get(event.type);
    if (handlers) {
      for (const handler of handlers) {
        promises.push(handler(event));
      }
    }
    await Promise.all(promises);
    return true;
  }
}
