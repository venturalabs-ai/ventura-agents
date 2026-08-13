export type ContextSource = Readonly<{ id: string; content: string; relevance: number; tokens: number }>;
export type CompiledContext = Readonly<{ content: string; sourceIds: readonly string[]; usedTokens: number; omitted: number }>;
export function compileContext(sources: readonly ContextSource[], tokenBudget: number): CompiledContext {
  if (!Number.isInteger(tokenBudget) || tokenBudget < 1) throw new Error("tokenBudget must be a positive integer");
  const selected: ContextSource[] = []; let usedTokens = 0;
  for (const source of [...sources].sort((a, b) => b.relevance - a.relevance || a.id.localeCompare(b.id))) {
    if (source.tokens < 0) throw new Error("source tokens cannot be negative");
    if (usedTokens + source.tokens <= tokenBudget) { selected.push(source); usedTokens += source.tokens; }
  }
  return { content: selected.map((source) => `[source:${source.id}]\n${source.content}`).join("\n\n"), sourceIds: selected.map((source) => source.id), usedTokens, omitted: sources.length - selected.length };
}
