import assert from "node:assert/strict";
import test from "node:test";
import { agents, findAgent } from "../src/catalog.js";
test("contains every platform layer", () => assert.deepEqual(new Set(agents.map((agent) => agent.layer)), new Set(["data-engineering", "ai", "mlops", "agentops"])));
test("finds a registered agent", () => assert.equal(findAgent("mlops-operator")?.layer, "mlops"));
test("returns undefined for unknown agents", () => assert.equal(findAgent("unknown"), undefined));
