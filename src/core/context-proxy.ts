import { compileContext, type ContextSource } from "../platform/context.js";

export type EvidenceReference = Readonly<{ id: string; timestamp: string; type: string }>;

export type CompressedState = Readonly<{
  agentId: string;
  sessionId: string;
  phase: string;
  current: Readonly<{
    pendingApprovals: readonly string[];
    activeIssues: readonly string[];
    keyDecisions: readonly string[];
  }>;
  metadata: Readonly<{
    totalMessages: number;
    totalCost: number;
    lastUpdated: string;
  }>;
  evidence: Readonly<{ references: readonly EvidenceReference[] }>;
}>;

export type StateDelta = Readonly<{
  phase?: string;
  pendingApprovals?: readonly string[];
  activeIssues?: readonly string[];
  decision?: string;
  evidence?: EvidenceReference;
  cost?: number;
}>;

export type CompiledAgentContext = Readonly<{
  content: string;
  sourceIds: readonly string[];
  usedTokens: number;
  omitted: number;
  totalTokens: number;
  compressionRatio: number;
}>;

export type ContextProxyConfig = Readonly<{
  maxContextSize: number;
  maxKeyDecisions?: number;
  maxEvidenceRefs?: number;
}>;

/**
 * Context Proxy — manages a bounded, deterministic compressed state per
 * agent/session instead of a full conversation history. Context assembly is
 * budget-driven and provider-agnostic (no Redis, no LLM), aligning with
 * ADR-0001 platform primitives.
 */
export class ContextProxy {
  private readonly states = new Map<string, CompressedState>();

  constructor(private readonly config: ContextProxyConfig) {}

  private key(agentId: string, sessionId: string): string {
    return `${agentId}:${sessionId}`;
  }

  createState(agentId: string, sessionId: string, phase: string): CompressedState {
    const state: CompressedState = {
      agentId,
      sessionId,
      phase,
      current: { pendingApprovals: [], activeIssues: [], keyDecisions: [] },
      metadata: { totalMessages: 0, totalCost: 0, lastUpdated: new Date(0).toISOString() },
      evidence: { references: [] },
    };
    this.states.set(this.key(agentId, sessionId), state);
    return state;
  }

  getState(agentId: string, sessionId: string): CompressedState | undefined {
    return this.states.get(this.key(agentId, sessionId));
  }

  /**
   * Applies a delta and stores only a bounded window (last N decisions,
   * last M evidence references). The returned state is a new immutable value.
   */
  updateState(agentId: string, sessionId: string, delta: StateDelta): CompressedState {
    const previous = this.states.get(this.key(agentId, sessionId));
    if (!previous) throw new Error("state not found; call createState first");

    const maxDecisions = this.config.maxKeyDecisions ?? 5;
    const maxEvidence = this.config.maxEvidenceRefs ?? 50;
    const keyDecisions = delta.decision
      ? [...previous.current.keyDecisions, delta.decision].slice(-maxDecisions)
      : previous.current.keyDecisions;
    const references = delta.evidence
      ? [...previous.evidence.references, delta.evidence].slice(-maxEvidence)
      : previous.evidence.references;

    const state: CompressedState = {
      agentId,
      sessionId,
      phase: delta.phase ?? previous.phase,
      current: {
        pendingApprovals: delta.pendingApprovals ?? previous.current.pendingApprovals,
        activeIssues: delta.activeIssues ?? previous.current.activeIssues,
        keyDecisions,
      },
      metadata: {
        totalMessages: previous.metadata.totalMessages + 1,
        totalCost: previous.metadata.totalCost + (delta.cost ?? 0),
        lastUpdated: new Date().toISOString(),
      },
      evidence: { references },
    };
    this.states.set(this.key(agentId, sessionId), state);
    return state;
  }

  /**
   * Deterministic budget-driven context assembly. Relevance is computed from
   * lexical overlap with the message; no provider call is made.
   */
  compileContext(agentId: string, sessionId: string, message: string, tokenBudget: number): CompiledAgentContext {
    const state = this.states.get(this.key(agentId, sessionId));
    if (!state) throw new Error("state not found; call createState first");

    const messageTokens = this.tokens(message);
    const sources: ContextSource[] = [];
    const push = (id: string, content: string, relevance: number): void => {
      sources.push({ id, content, relevance, tokens: this.estimateTokens(content) });
    };

    push("phase", `phase: ${state.phase}`, 0.2);
    if (state.current.pendingApprovals.length > 0) {
      push("pendingApprovals", `pending approvals: ${state.current.pendingApprovals.join(", ")}`, 0.8);
    }
    if (state.current.activeIssues.length > 0) {
      push("activeIssues", `active issues: ${state.current.activeIssues.join(", ")}`, 0.9);
    }
    if (state.current.keyDecisions.length > 0) {
      push("keyDecisions", `decisions: ${state.current.keyDecisions.join(" | ")}`, 0.7);
    }
    for (const ref of state.evidence.references) {
      const overlap = this.overlap(messageTokens, this.tokens(ref.id));
      if (overlap > 0) {
        push(ref.id, `[evidence:${ref.type}] ${ref.id} @ ${ref.timestamp}`, 0.5 + Math.min(overlap, 3) * 0.1);
      }
    }

    const selected = compileContext(sources, tokenBudget);
    const fullTokens =
      sources.reduce((sum, source) => sum + source.tokens, 0) + this.estimateTokens(message);
    const usedTokens = selected.usedTokens + this.estimateTokens(message);
    return {
      content: selected.content ? `${selected.content}\n\nmessage: ${message}` : `message: ${message}`,
      sourceIds: selected.sourceIds,
      usedTokens,
      omitted: selected.omitted,
      totalTokens: fullTokens,
      compressionRatio: fullTokens === 0 ? 1 : Number((usedTokens / fullTokens).toFixed(4)),
    };
  }

  chunkItems<T>(items: readonly T[], batchSize: number): readonly (readonly T[])[] {
    if (!Number.isInteger(batchSize) || batchSize < 1) throw new Error("batchSize must be a positive integer");
    const batches: T[][] = [];
    for (let i = 0; i < items.length; i += batchSize) {
      batches.push(items.slice(i, i + batchSize));
    }
    return batches;
  }

  private estimateTokens(text: string): number {
    return Math.max(1, Math.ceil(text.length / 4));
  }

  private tokens(text: string): ReadonlySet<string> {
    return new Set(text.toLowerCase().match(/[a-z0-9_]+/g) ?? []);
  }

  private overlap(left: ReadonlySet<string>, right: ReadonlySet<string>): number {
    let count = 0;
    for (const token of left) {
      if (right.has(token)) count += 1;
    }
    return count;
  }
}
