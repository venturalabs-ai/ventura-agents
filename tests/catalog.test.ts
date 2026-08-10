import assert from "node:assert/strict";
import test from "node:test";
import { agents, findAgent } from "../src/catalog.js";
test("contains every operational agent layer", () => assert.deepEqual(new Set(agents.map((agent) => agent.layer)), new Set(["coordination", "delivery", "data-engineering", "ai", "security", "mlops", "agentops"])));
test("agent identifiers are unique", () => assert.equal(new Set(agents.map((agent) => agent.id)).size, agents.length));
test("finds a registered agent", () => assert.equal(findAgent("mlops-operator")?.layer, "mlops"));
test("returns undefined for unknown agents", () => assert.equal(findAgent("unknown"), undefined));
