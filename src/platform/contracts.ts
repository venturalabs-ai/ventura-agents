export type TraceContext = Readonly<{ traceId: string; sessionId: string; actorId: string }>;
export type Budget = Readonly<{ maxTokens: number; maxCostUsd: number; deadlineMs: number }>;
export type Approval = Readonly<{ required: boolean; reason?: string }>;

export interface PolicyDecision {
  allowed: boolean;
  approval: Approval;
  reasons: readonly string[];
}

export interface PolicyEngine {
  evaluate(action: string, context: TraceContext, budget: Budget): Promise<PolicyDecision>;
}

export interface ModelRoute {
  provider: string;
  model: string;
  reason: string;
}

export interface ModelRouter {
  select(task: string, budget: Budget): Promise<ModelRoute>;
}

export interface AgentTask<Input = unknown> {
  id: string;
  kind: string;
  input: Input;
  context: TraceContext;
  budget: Budget;
}

export interface AgentResult<Output = unknown> {
  taskId: string;
  status: "succeeded" | "failed" | "awaiting-approval";
  output?: Output;
  evidence: readonly string[];
  costUsd: number;
}

export interface Orchestrator {
  execute<Input, Output>(task: AgentTask<Input>): Promise<AgentResult<Output>>;
}
