#!/usr/bin/env node
/**
 * Perplexity MCP Server
 * Wraps Perplexity API as an MCP stdio server
 */
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { CallToolRequestSchema, ListToolsRequestSchema } = require('@modelcontextprotocol/sdk/types.js');

const API_KEY = process.env.PERPLEXITY_API_KEY;
if (!API_KEY) {
  console.error('PERPLEXITY_API_KEY env var required');
  process.exit(1);
}

const server = new Server({
  name: 'perplexity-search',
  version: '1.0.0'
}, {
  capabilities: { tools: {} }
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: 'search',
    description: 'Search the web using Perplexity AI',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Search query' },
        count: { type: 'number', description: 'Number of results (1-10)', default: 5 },
        freshness: { type: 'string', description: 'Recency filter: pd (past day), pw (past week), pm (past month), py (past year)', enum: ['pd', 'pw', 'pm', 'py'] }
      },
      required: ['query']
    }
  }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === 'search') {
    const { query, count = 5, freshness } = request.params.arguments;
    
    const response = await fetch('https://api.perplexity.ai/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'sonar',
        messages: [{ role: 'user', content: query }],
        max_tokens: 2000
      })
    });
    
    if (!response.ok) {
      const err = await response.text();
      return { content: [{ type: 'text', text: `Error: ${err}` }], isError: true };
    }
    
    const data = await response.json();
    const result = data.choices?.[0]?.message?.content || 'No response';
    const citations = data.citations?.map((c, i) => `[${i + 1}] ${c}`).join('\n') || '';
    
    return {
      content: [{
        type: 'text',
        text: citations ? `${result}\n\nSources:\n${citations}` : result
      }]
    };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

const transport = new StdioServerTransport();
server.connect(transport);
console.error('Perplexity MCP server running');
