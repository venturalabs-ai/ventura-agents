export type ContextSource = Readonly<{ id: string; content: string; relevance: number; tokens: number }>;
export type CompiledContext = Readonly<{ content: string; sourceIds: readonly string[]; usedTokens: number; omitted: number }>;
export function compileContext(sources: readonly ContextSource[], tokenBudget: number): CompiledContext {
  if (!Number.isInteger(tokenBudget) || tokenBudget < 1) throw new Error("tokenBudget must be a positive integer");
  const selected: ContextSource[] = [];
  let usedTokens = 0;

  // Slice to create a shallow copy and sort in-place, avoiding spread operator overhead
  const sortedSources = sources.slice().sort((a, b) => b.relevance - a.relevance || a.id.localeCompare(b.id));

  for (let i = 0; i < sortedSources.length; i++) {
    const source = sortedSources[i]!;
    if (source.tokens < 0) throw new Error("source tokens cannot be negative");
    if (usedTokens + source.tokens <= tokenBudget) {
      selected.push(source);
      usedTokens += source.tokens;
    }
  }

  let content = "";
  const sourceIds: string[] = [];

  // Construct output iteratively instead of allocating multiple intermediate arrays with .map().join()
  for (let i = 0; i < selected.length; i++) {
    const source = selected[i]!;
    if (i > 0) content += "\n\n";
    content += `[source:${source.id}]\n${source.content}`;
    sourceIds.push(source.id);
  }

  return { content, sourceIds, usedTokens, omitted: sources.length - selected.length };
}
