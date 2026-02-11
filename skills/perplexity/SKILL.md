---
name: perplexity
description: Perplexity AI search - replaces native web_search with Perplexity's Sonar model
metadata:
  openclaw:
    emoji: 🔍
    requires:
      env:
        - PERPLEXITY_API_KEY
---

# Perplexity Search

Uses Perplexity AI (Sonar model) for web search with inline citations.

## Setup

API key stored in:
- `~/.bashrc` as `PERPLEXITY_API_KEY`
- OpenClaw config: `auth.profiles.perplexity`

## Usage

```bash
# Direct MCP
mcporter call perplexity.search query="your search"

# Wrapper script
perplexity-search "your query"
```

## Available Tools

- `perplexity.search` - Web search with citations
  - `query` (required): Search string
  - `count`: Number of results (default: 5)
  - `freshness`: pd (past day), pw (week), pm (month), py (year)

## Examples

```bash
mcporter call perplexity.search query="AI news today" freshness=pd
mcporter call perplexity.search query="Python asyncio best practices" count=10
```
