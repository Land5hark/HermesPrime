import { NextResponse } from 'next/server';
import fs from 'fs/promises';
import path from 'path';

const WORKSPACE_ROOT = '/home/clawd/.openclaw/workspace';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const filePath = searchParams.get('path');
  
  if (!filePath) {
    return NextResponse.json({ error: 'Path required' }, { status: 400 });
  }
  
  // Security: prevent directory traversal
  const safePath = path.normalize(filePath).replace(/^(\.\.(\/|$))+/, '');
  const fullPath = path.join(WORKSPACE_ROOT, safePath);
  
  // Ensure we don't escape workspace
  if (!fullPath.startsWith(WORKSPACE_ROOT)) {
    return NextResponse.json({ error: 'Invalid path' }, { status: 400 });
  }
  
  try {
    const stats = await fs.stat(fullPath);
    
    if (stats.isDirectory()) {
      return NextResponse.json({ error: 'Path is a directory' }, { status: 400 });
    }
    
    // Check file size (limit to 5MB for text files)
    if (stats.size > 5 * 1024 * 1024) {
      return NextResponse.json({ 
        error: 'File too large',
        size: stats.size,
      }, { status: 413 });
    }
    
    const content = await fs.readFile(fullPath, 'utf-8');
    const extension = path.extname(filePath).toLowerCase();
    
    // Determine content type
    let contentType = 'text';
    if (['.md', '.markdown'].includes(extension)) contentType = 'markdown';
    else if (['.json'].includes(extension)) contentType = 'json';
    else if (['.js', '.ts', '.jsx', '.tsx', '.py', '.rb', '.go', '.rs', '.java', '.c', '.cpp', '.h'].includes(extension)) contentType = 'code';
    else if (['.html', '.htm', '.xml'].includes(extension)) contentType = 'html';
    else if (['.css', '.scss', '.sass', '.less'].includes(extension)) contentType = 'css';
    else if (['.yaml', '.yml', '.toml'].includes(extension)) contentType = 'config';
    
    return NextResponse.json({
      path: safePath,
      name: path.basename(filePath),
      content,
      contentType,
      size: stats.size,
      modified: stats.mtime.toISOString(),
    });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Failed to read file' },
      { status: 500 }
    );
  }
}
