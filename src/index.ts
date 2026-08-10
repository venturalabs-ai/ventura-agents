import { createServer } from "node:http";
import { agents, findAgent } from "./catalog.js";
import { capabilities, capabilitySummary } from "./platform/architecture.js";
const port = Number(process.env.PORT ?? 3001);
const server = createServer((req, res) => {
  res.setHeader("content-type", "application/json; charset=utf-8");
  if (req.method === "GET" && req.url === "/health") return void res.end(JSON.stringify({ status: "ok", service: "ventura-global-agents" }));
  if (req.method === "GET" && req.url === "/v1/agents") return void res.end(JSON.stringify({ agents }));
  if (req.method === "GET" && req.url === "/v1/platform/capabilities") return void res.end(JSON.stringify({ capabilities, summary: capabilitySummary() }));
  if (req.method === "GET" && req.url?.startsWith("/v1/agents/")) {
    const agent = findAgent(decodeURIComponent(req.url.slice(11))); res.statusCode = agent ? 200 : 404; return void res.end(JSON.stringify(agent ?? { error: "agent not found" }));
  }
  res.statusCode = 404; res.end(JSON.stringify({ error: "not found" }));
});
server.listen(port, "0.0.0.0", () => console.log(JSON.stringify({ event: "catalog.started", port })));
