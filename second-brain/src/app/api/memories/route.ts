import { NextResponse } from 'next/server';
import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';

const WORKSPACE_ROOT = '/home/clawd/.openclaw/workspace';

export async function GET() {
  try {
    const memories = [];
    
    // Read main MEMORY.md
    const mainMemoryPath = path.join(WORKSPACE_ROOT, 'MEMORY.md');
    try {
      const mainContent = await fs.readFile(mainMemoryPath, 'utf-8');
      const stats = await fs.stat(mainMemoryPath);
      memories.push({
        id: 'main',
        title: 'Main Memory (Curated)',
        date: stats.mtime.toISOString(),
        content: mainContent,
        type: 'curated',
      });
    } catch (e) {
      console.error('Error reading main memory:', e);
    }
    
    // Read daily memory files
    const memoryDir = path.join(WORKSPACE_ROOT, 'memory');
    try {
      const files = await fs.readdir(memoryDir);
      const mdFiles = files.filter(f => f.endsWith('.md')).sort().reverse();
      
      for (const file of mdFiles.slice(0, 50)) { // Limit to 50 most recent
        const filePath = path.join(memoryDir, file);
        const content = await fs.readFile(filePath, 'utf-8');
        const stats = await fs.stat(filePath);
        
        // Parse date from filename (YYYY-MM-DD) or use file mtime
        const dateMatch = file.match(/(\d{4}-\d{2}-\d{2})/);
        const date = dateMatch ? `${dateMatch[1]}T00:00:00Z` : stats.mtime.toISOString();
        
        memories.push({
          id: file.replace('.md', ''),
          title: file.replace('.md', '').replace(/-/g, ' '),
          date,
          content: content.slice(0, 5000), // Limit content length
          type: 'daily',
        });
      }
    } catch (e) {
      console.error('Error reading memory directory:', e);
    }
    
    return NextResponse.json({ memories });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch memories' },
      { status: 500 }
    );
  }
}
