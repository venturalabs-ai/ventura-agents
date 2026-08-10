export type AgentLayer = "coordination" | "delivery" | "data-engineering" | "ai" | "security" | "mlops" | "agentops";
export type Agent = Readonly<{ id: string; layer: AgentLayer; capability: string; version: string }>;
export const agents: readonly Agent[] = [
  { id: "supervisor", layer: "coordination", capability: "delegation, budgets and termination", version: "1.0.0" },
  { id: "planner", layer: "coordination", capability: "task decomposition and dependency planning", version: "1.0.0" },
  { id: "researcher", layer: "delivery", capability: "evidence retrieval and source synthesis", version: "1.0.0" },
  { id: "coder", layer: "delivery", capability: "implementation and test generation", version: "1.0.0" },
  { id: "reviewer", layer: "delivery", capability: "quality and risk review", version: "1.0.0" },
  { id: "validator", layer: "delivery", capability: "acceptance criteria and evidence validation", version: "1.0.0" },
  { id: "pipeline-engineer", layer: "data-engineering", capability: "batch and streaming pipelines", version: "1.0.0" },
  { id: "ai-engineer", layer: "ai", capability: "retrieval and model integration", version: "1.0.0" },
  { id: "security-specialist", layer: "security", capability: "threat analysis, policy and security gates", version: "1.0.0" },
  { id: "architect", layer: "coordination", capability: "architecture decisions and boundary governance", version: "1.0.0" },
  { id: "mlops-operator", layer: "mlops", capability: "model lifecycle and deployment", version: "1.0.0" },
  { id: "agentops-observer", layer: "agentops", capability: "traces, evaluations and cost", version: "1.0.0" }
];
export function findAgent(id: string): Agent | undefined { return agents.find((agent) => agent.id === id); }
