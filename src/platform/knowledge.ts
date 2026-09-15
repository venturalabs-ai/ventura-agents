export type Ontology = Readonly<{ entityTypes: readonly string[]; relations: Readonly<Record<string, readonly string[]>> }>;
export type Entity = Readonly<{ id: string; type: string; attributes?: Readonly<Record<string, unknown>> }>;
export type Edge = Readonly<{ from: string; relation: string; to: string }>;
export class KnowledgeGraph {
  private readonly entities = new Map<string, Entity>();
  private readonly edges: Edge[] = [];
  private readonly outgoingEdges = new Map<string, Edge[]>();

  constructor(private readonly ontology: Ontology) {}
  addEntity(entity: Entity): void {
    if (!this.ontology.entityTypes.includes(entity.type)) throw new Error(`unknown entity type: ${entity.type}`);
    this.entities.set(entity.id, entity);
  }
  connect(edge: Edge): void {
    const from = this.entities.get(edge.from); const to = this.entities.get(edge.to);
    if (!from || !to) throw new Error("both entities must exist");
    if (!(this.ontology.relations[from.type] ?? []).includes(edge.relation)) throw new Error(`relation ${edge.relation} is not allowed for ${from.type}`);
    this.edges.push(edge);

    let edgesFrom = this.outgoingEdges.get(edge.from);
    if (!edgesFrom) {
      edgesFrom = [];
      this.outgoingEdges.set(edge.from, edgesFrom);
    }
    edgesFrom.push(edge);
  }
  neighbors(id: string, relation?: string): readonly Entity[] {
    const results: Entity[] = [];
    const edgesFromId = this.outgoingEdges.get(id) ?? [];
    for (const edge of edgesFromId) {
      if (!relation || edge.relation === relation) {
        const entity = this.entities.get(edge.to);
        if (entity) results.push(entity);
      }
    }
    return results;
  }
}
