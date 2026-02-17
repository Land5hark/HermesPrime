import { NextResponse } from 'next/server';
import fs from 'fs/promises';
import path from 'path';

const WORKSPACE_ROOT = '/home/clawd/.openclaw/workspace';

interface FileEntry {
  name: string;
  path: string;
  type: 'file' | 'directory';
  size?: number;
  modified?: string;
  extension?: string;
}

async function scanDirectory(dirPath: string, relativePath: string = ''): Promise<FileEntry[]> {
  const entries: FileEntry[] = [];
  
  try {
    const items = await fs.readdir(dirPath, { withFileTypes: true });
    
    for (const item of items) {
      // Skip hidden files and common non-document directories
      if (item.name.startsWith('.') || 
          item.name === 'node_modules' || 
          item.name === '.git' ||
          item.name === 'dist' ||
          item.name === 'build') {
        continue;
      }
      
      const fullPath = path.join(dirPath, item.name);
      const itemRelativePath = path.join(relativePath, item.name);
      
      if (item.isDirectory()) {
        entries.push({
          name: item.name,
          path: itemRelativePath,
          type: 'directory',
        });
      } else {
        const stats = await fs.stat(fullPath);
        const ext = path.extname(item.name).toLowerCase();
        entries.push({
          name: item.name,
          path: itemRelativePath,
          type: 'file',
          size: stats.size,
          modified: stats.mtime.toISOString(),
          extension: ext,
        });
      }
    }
  } catch (e) {
    console.error(`Error scanning ${dirPath}:`, e);
  }
  
  // Sort: directories first, then files alphabetically
  return entries.sort((a, b) => {
    if (a.type === b.type) return a.name.localeCompare(b.name);
    return a.type === 'directory' ? -1 : 1;
  });
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const scanPath = searchParams.get('path') || '';
  
  // Security: prevent directory traversal
  const safePath = path.normalize(scanPath).replace(/^(\.\.(\/|$))+/, '');
  const fullPath = path.join(WORKSPACE_ROOT, safePath);
  
  // Ensure we don't escape workspace
  if (!fullPath.startsWith(WORKSPACE_ROOT)) {
    return NextResponse.json({ error: 'Invalid path' }, { status: 400 });
  }
  
  try {
    const entries = await scanDirectory(fullPath, safePath);
    
    return NextResponse.json({
      path: safePath,
      entries,
    });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Failed to scan directory' },
      { status: 500 }
    );
  }
}
