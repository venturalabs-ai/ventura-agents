export type Maturity = "implemented" | "contract" | "planned";

export type PlatformCapability = Readonly<{
  id: string;
  domain: string;
  maturity: Maturity;
  evidence: readonly string[];
}>;

export const capabilities: readonly PlatformCapability[] = [
  { id: "orchestration-engine", domain: "core", maturity: "contract", evidence: ["src/platform/contracts.ts"] },
  { id: "multi-agent-system", domain: "agents", maturity: "implemented", evidence: ["src/catalog.ts", "tests/catalog.test.ts"] },
  { id: "mcp", domain: "protocols", maturity: "planned", evidence: ["docs/MCP_FOR_AGENTS.md"] },
  { id: "a2a", domain: "protocols", maturity: "planned", evidence: [] },
  { id: "vector-database", domain: "memory", maturity: "contract", evidence: ["src/rag/pipeline.py"] },
  { id: "knowledge-graph", domain: "memory", maturity: "planned", evidence: [] },
  { id: "rag-pipeline", domain: "rag", maturity: "contract", evidence: ["src/rag/pipeline.py", "tests/test_rag_contract.py"] },
  { id: "model-routing", domain: "models", maturity: "contract", evidence: ["src/platform/contracts.ts"] },
  { id: "evals", domain: "evals", maturity: "contract", evidence: ["tests/platform.test.ts"] },
  { id: "data-platform", domain: "data-platform", maturity: "planned", evidence: [] },
  { id: "connectors", domain: "connectors", maturity: "planned", evidence: [] },
  { id: "mlops", domain: "mlops", maturity: "contract", evidence: ["src/catalog.ts"] },
  { id: "agentops", domain: "agentops", maturity: "contract", evidence: ["src/catalog.ts", "ops/otel-collector.yml"] },
  { id: "security-governance", domain: "security", maturity: "contract", evidence: ["src/platform/contracts.ts"] },
  { id: "observability", domain: "observability", maturity: "contract", evidence: ["ops/otel-collector.yml", "docker-compose.yml"] },
  { id: "human-in-the-loop", domain: "human-loop", maturity: "contract", evidence: ["src/platform/contracts.ts"] },
  { id: "deployment", domain: "deployment", maturity: "implemented", evidence: ["Dockerfile", "docker-compose.yml", ".github/workflows/ci.yml"] }
];

export function capabilitySummary() {
  return capabilities.reduce<Record<Maturity, number>>((summary, capability) => {
    summary[capability.maturity] += 1;
    return summary;
  }, { implemented: 0, contract: 0, planned: 0 });
}
