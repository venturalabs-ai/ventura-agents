import assert from "node:assert/strict";
import test from "node:test";
import { AgentRegistry, ApprovalQueue, EventBus, KnowledgeGraph, assessRisk, compileContext } from "../src/platform/index.js";
test("event bus delivers once by event id", async () => {
  const bus = new EventBus(); let deliveries = 0; bus.subscribe("run.created", () => { deliveries += 1; });
  const event = { id: "evt-1", type: "run.created", occurredAt: new Date(0).toISOString(), payload: {} };
  assert.equal(await bus.publish(event), true); assert.equal(await bus.publish(event), false); assert.equal(deliveries, 1);
});
test("context compiler respects budget and relevance", () => {
  const result = compileContext([{ id: "a", content: "A", relevance: 0.9, tokens: 7 }, { id: "b", content: "B", relevance: 0.8, tokens: 5 }], 7);
  assert.deepEqual(result.sourceIds, ["a"]); assert.equal(result.usedTokens, 7); assert.equal(result.omitted, 1);
});
test("knowledge graph enforces ontology", () => {
  const graph = new KnowledgeGraph({ entityTypes: ["agent", "capability"], relations: { agent: ["provides"] } });
  graph.addEntity({ id: "a", type: "agent" }); graph.addEntity({ id: "c", type: "capability" }); graph.connect({ from: "a", relation: "provides", to: "c" });
  assert.equal(graph.neighbors("a", "provides")[0]?.id, "c"); assert.throws(() => graph.addEntity({ id: "x", type: "unknown" }), /unknown entity type/);
});
test("risk policy blocks critical operations", () => assert.deepEqual(assessRisk({ impact: 5, likelihood: 5, detectability: 5, sensitiveData: true }), { score: 145, level: "critical", action: "block" }));
test("human loop records accountable decisions", () => {
  const queue = new ApprovalQueue(); const pending = queue.request("run-1", "high risk");
  assert.equal(queue.pending().length, 1); assert.equal(queue.decide(pending.id, "approved", "reviewer@example.com").decidedBy, "reviewer@example.com"); assert.equal(queue.pending().length, 0);
});
test("agent registry discovers only active capable agents", () => {
  const registry = new AgentRegistry();
  registry.register({ id: "data-agent", version: "1.0.0", capabilities: ["etl"], endpoint: "http://data-agent:8080", status: "active" });
  registry.register({ id: "old-agent", version: "1.0.0", capabilities: ["etl"], endpoint: "http://old:8080", status: "offline" });
  assert.deepEqual(registry.resolve("etl").map((agent) => agent.id), ["data-agent"]);
});
