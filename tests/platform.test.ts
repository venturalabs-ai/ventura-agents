import assert from "node:assert/strict";
import test from "node:test";
import { capabilities, capabilitySummary } from "../src/platform/architecture.js";

test("world-class capability identifiers are unique", () => {
  assert.equal(new Set(capabilities.map(({ id }) => id)).size, capabilities.length);
});

test("implemented capabilities have repository evidence", () => {
  for (const capability of capabilities.filter(({ maturity }) => maturity === "implemented")) {
    assert.ok(capability.evidence.length > 0, `${capability.id} must declare evidence`);
  }
});

test("maturity summary accounts for every capability", () => {
  const summary = capabilitySummary();
  assert.equal(summary.implemented + summary.contract + summary.planned, capabilities.length);
});
