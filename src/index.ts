import { createServer } from "node:http";
import { agents, findAgent } from "./catalog.js";

const port = Number(process.env.PORT ?? 3001);
const version = process.env.npm_package_version ?? "3.0.0";

const server = createServer((req, res) => {
  res.setHeader("content-type", "application/json; charset=utf-8");

  if (req.method === "GET" && req.url === "/health") {
    return void res.end(
      JSON.stringify({
        status: "operational",
        service: "ventura-agents",
        version,
        timestamp: new Date().toISOString(),
        agents: {
          catalog_size: agents.length,
        },
      }),
    );
  }

  if (req.method === "GET" && req.url === "/v1/agents") {
    return void res.end(JSON.stringify({ agents }));
  }

  if (req.method === "GET" && req.url?.startsWith("/v1/agents/")) {
    let agentId: string;
    try {
      agentId = decodeURIComponent(req.url.slice(11));
    } catch {
      res.statusCode = 400;
      return void res.end(JSON.stringify({ error: "invalid agent id" }));
    }
    const agent = findAgent(agentId);
    res.statusCode = agent ? 200 : 404;
    return void res.end(JSON.stringify(agent ?? { error: "agent not found" }));
  }

  res.statusCode = 404;
  res.end(JSON.stringify({ error: "not found" }));
});

server.listen(port, "0.0.0.0", () =>
  console.log(JSON.stringify({ event: "catalog.started", port, version })),
);
