export type RiskInput = Readonly<{ impact: number; likelihood: number; detectability: number; sensitiveData: boolean }>;
export type RiskDecision = Readonly<{ score: number; level: "low" | "medium" | "high" | "critical"; action: "allow" | "review" | "block" }>;
export function assessRisk(input: RiskInput): RiskDecision {
  for (const value of [input.impact, input.likelihood, input.detectability]) if (!Number.isFinite(value) || value < 1 || value > 5) throw new Error("risk factors must be between 1 and 5");
  const score = input.impact * input.likelihood * input.detectability + (input.sensitiveData ? 20 : 0);
  const level = score >= 80 ? "critical" : score >= 45 ? "high" : score >= 20 ? "medium" : "low";
  return { score, level, action: level === "critical" ? "block" : level === "high" ? "review" : "allow" };
}
