# Perplexity Search Skill

Replaces the native `web_search` tool with Perplexity AI.

## Usage

```bash
# Direct MCP call
mcporter call perplexity.search query="your search here"

# Via skill wrapper (automatic)
web_search "your query"
```

## Environment

Set `PERPLEXITY_API_KEY` in your shell or gateway env.

## Testing

```bash
export PERPLEXITY_API_KEY=pplx-...
mcporter call perplexity.search query="latest AI news" count=5
```
