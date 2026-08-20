import assert from "node:assert/strict";
import test from "node:test";
import { ContextProxy } from "../src/core/context-proxy.js";

test("creates an empty bounded state", () => {
  const proxy = new ContextProxy({ maxContextSize: 1000 });
  const state = proxy.createState("agent-1", "session-1", "extract");
  assert.equal(state.current.keyDecisions.length, 0);
  assert.equal(state.metadata.totalMessages, 0);
});

test("updateState keeps only the last N decisions", () => {
  const proxy = new ContextProxy({ maxContextSize: 1000, maxKeyDecisions: 2 });
  proxy.createState("agent-1", "session-1", "extract");
  for (const decision of ["d1", "d2", "d3"]) {
    proxy.updateState("agent-1", "session-1", { decision });
  }
  const state = proxy.getState("agent-1", "session-1");
  assert.deepEqual(state?.current.keyDecisions, ["d2", "d3"]);
});

test("updateState bounds evidence references", () => {
  const proxy = new ContextProxy({ maxContextSize: 1000, maxEvidenceRefs: 1 });
  proxy.createState("agent-1", "session-1", "extract");
  proxy.updateState("agent-1", "session-1", { evidence: { id: "doc-a", timestamp: new Date(0).toISOString(), type: "source" } });
  proxy.updateState("agent-1", "session-1", { evidence: { id: "doc-b", timestamp: new Date(0).toISOString(), type: "source" } });
  assert.deepEqual(proxy.getState("agent-1", "session-1")?.evidence.references.map((ref) => ref.id), ["doc-b"]);
});

test("compileContext selects relevant evidence within the budget", () => {
  const proxy = new ContextProxy({ maxContextSize: 1000 });
  proxy.createState("agent-1", "session-1", "extract");
  proxy.updateState("agent-1", "session-1", { evidence: { id: "invoice-fiscal", timestamp: new Date(0).toISOString(), type: "tax" } });
  proxy.updateState("agent-1", "session-1", { evidence: { id: "payroll-hr", timestamp: new Date(0).toISOString(), type: "hr" } });
  const context = proxy.compileContext("agent-1", "session-1", "audit invoice", 10_000);
  assert.ok(context.sourceIds.includes("invoice-fiscal"));
  assert.ok(context.content.includes("message: audit invoice"));
});

test("compileContext compresses long histories", () => {
  const proxy = new ContextProxy({ maxContextSize: 1000 });
  proxy.createState("agent-1", "session-1", "extract");
  for (let i = 0; i < 100; i += 1) {
    proxy.updateState("agent-1", "session-1", {
      decision: `decision ${i}: approve tax reconciliation invoice for fiscal audit period 2026`,
    });
  }
  const context = proxy.compileContext("agent-1", "session-1", "final report", 50);
  assert.ok(context.omitted > 0);
  assert.ok(context.compressionRatio > 0 && context.compressionRatio < 1);
});

test("compileContext throws when the session was never created", () => {
  const proxy = new ContextProxy({ maxContextSize: 1000 });
  assert.throws(() => proxy.compileContext("agent-1", "missing", "hi", 1000), /state not found/);
});

test("chunkItems partitions deterministically and validates batch size", () => {
  const proxy = new ContextProxy({ maxContextSize: 1000 });
  const batches = proxy.chunkItems([1, 2, 3, 4, 5, 6, 7], 3);
  assert.deepEqual(batches, [[1, 2, 3], [4, 5, 6], [7]]);
  assert.throws(() => proxy.chunkItems([1], 0), /batchSize must be a positive integer/);
});
