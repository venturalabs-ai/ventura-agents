export type AgentLayer = "data-engineering" | "ai" | "mlops" | "agentops";
export type Agent = Readonly<{ id: string; layer: AgentLayer; capability: string; version: string }>;
export const agents: readonly Agent[] = [
  { id: "pipeline-engineer", layer: "data-engineering", capability: "batch and streaming pipelines", version: "1.0.0" },
  { id: "ai-engineer", layer: "ai", capability: "retrieval and model integration", version: "1.0.0" },
  { id: "mlops-operator", layer: "mlops", capability: "model lifecycle and deployment", version: "1.0.0" },
  { id: "agentops-observer", layer: "agentops", capability: "traces, evaluations and cost", version: "1.0.0" }
];
export function findAgent(id: string): Agent | undefined { return agents.find((agent) => agent.id === id); }
