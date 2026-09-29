export type AgentRegistration = Readonly<{ id: string; version: string; capabilities: readonly string[]; endpoint: string; status: "active" | "draining" | "offline" }>;
export class AgentRegistry {
  private readonly registrations = new Map<string, AgentRegistration>();
  register(agent: AgentRegistration): void {
    if (!agent.id.trim() || !/^\d+\.\d+\.\d+$/.test(agent.version)) throw new Error("valid id and semantic version are required");
    if (!agent.capabilities.length || !agent.endpoint.startsWith("http")) throw new Error("capabilities and HTTP endpoint are required");
    this.registrations.set(`${agent.id}@${agent.version}`, agent);
  }
  resolve(capability: string): readonly AgentRegistration[] {
    // ⚡ Bolt: Iterating directly over Map values avoids O(N) intermediate array
    // allocation that occurs when using spread syntax [...map.values()].filter(...)
    const resolved: AgentRegistration[] = [];
    for (const agent of this.registrations.values()) {
      if (agent.status === "active" && agent.capabilities.includes(capability)) {
        resolved.push(agent);
      }
    }
    return resolved;
  }
}
