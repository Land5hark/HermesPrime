'use client';

import { useState, useEffect } from 'react';
import { marked } from 'marked';
import { 
  Folder, 
  File, 
  ChevronRight, 
  ChevronLeft,
  FileText,
  FileCode,
  FileJson,
  FileType,
  Clock,
  HardDrive
} from 'lucide-react';

interface FileEntry {
  name: string;
  path: string;
  type: 'file' | 'directory';
  size?: number;
  modified?: string;
  extension?: string;
}

interface FileContent {
  path: string;
  name: string;
  content: string;
  contentType: string;
  size: number;
  modified: string;
}

export default function DocumentsPage() {
  const [currentPath, setCurrentPath] = useState('');
  const [entries, setEntries] = useState<FileEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedFile, setSelectedFile] = useState<FileContent | null>(null);
  const [breadcrumbs, setBreadcrumbs] = useState<string[]>([]);

  useEffect(() => {
    fetchDirectory(currentPath);
  }, [currentPath]);

  async function fetchDirectory(path: string) {
    setLoading(true);
    try {
      const res = await fetch(`/api/documents?path=${encodeURIComponent(path)}`);
      const data = await res.json();
      setEntries(data.entries || []);
      
      // Update breadcrumbs
      if (path) {
        setBreadcrumbs(path.split('/').filter(Boolean));
      } else {
        setBreadcrumbs([]);
      }
    } catch (error) {
      console.error('Failed to fetch directory:', error);
    } finally {
      setLoading(false);
    }
  }

  async function openFile(entry: FileEntry) {
    try {
      const res = await fetch(`/api/documents/file?path=${encodeURIComponent(entry.path)}`);
      if (res.ok) {
        const data = await res.json();
        setSelectedFile(data);
      } else {
        console.error('Failed to load file');
      }
    } catch (error) {
      console.error('Error opening file:', error);
    }
  }

  function navigateUp() {
    const parts = currentPath.split('/').filter(Boolean);
    parts.pop();
    setCurrentPath(parts.join('/'));
    setSelectedFile(null);
  }

  function navigateToBreadcrumb(index: number) {
    const path = breadcrumbs.slice(0, index + 1).join('/');
    setCurrentPath(path);
    setSelectedFile(null);
  }

  function getFileIcon(extension?: string) {
    const ext = extension?.toLowerCase();
    if (['.md', '.txt', '.doc', '.pdf'].includes(ext)) return <FileText className="w-5 h-5 text-blue-500" />;
    if (['.js', '.ts', '.jsx', '.tsx', '.py', '.go', '.rs', '.java'].includes(ext)) return <FileCode className="w-5 h-5 text-yellow-500" />;
    if (['.json'].includes(ext)) return <FileJson className="w-5 h-5 text-green-500" />;
    if (['.html', '.css', '.scss'].includes(ext)) return <FileType className="w-5 h-5 text-orange-500" />;
    return <File className="w-5 h-5 text-gray-500" />;
  }

  function formatSize(bytes?: number) {
    if (!bytes) return '-';
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  }

  function formatDate(dateStr?: string) {
    if (!dateStr) return '-';
    try {
      return new Date(dateStr).toLocaleString();
    } catch {
      return dateStr;
    }
  }

  if (loading && entries.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="flex h-full">
      {/* File Browser */}
      <div className="flex-1 flex flex-col">
        {/* Breadcrumb & Toolbar */}
        <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
          <div className="flex items-center gap-2 mb-4">
            {currentPath && (
              <button
                onClick={navigateUp}
                className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>
            )}
            <div className="flex items-center gap-1 text-sm">
              <button
                onClick={() => { setCurrentPath(''); setSelectedFile(null); }}
                className="text-blue-600 hover:underline"
              >
                Home
              </button>
              {breadcrumbs.map((crumb, idx) => (
                <span key={idx} className="flex items-center gap-1">
                  <ChevronRight className="w-4 h-4 text-gray-400" />
                  <button
                    onClick={() => navigateToBreadcrumb(idx)}
                    className="text-blue-600 hover:underline"
                  >
                    {crumb}
                  </button>
                </span>
              ))}
            </div>
          </div>
          
          {/* Column Headers */}
          <div className="grid grid-cols-[1fr,100px,180px] gap-4 text-sm font-medium text-gray-500 dark:text-gray-400 px-4">
            <span>Name</span>
            <span>Size</span>
            <span>Modified</span>
          </div>
        </div>
        
        {/* File List */}
        <div className="flex-1 overflow-y-auto bg-white dark:bg-gray-900">
          {entries.map((entry) => (
            <button
              key={entry.path}
              onClick={() => entry.type === 'directory' ? setCurrentPath(entry.path) : openFile(entry)}
              className="w-full grid grid-cols-[1fr,100px,180px] gap-4 px-4 py-3 border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800 text-left items-center"
            >
              <div className="flex items-center gap-3">
                {entry.type === 'directory' ? (
                  <Folder className="w-5 h-5 text-amber-500" />
                ) : (
                  getFileIcon(entry.extension)
                )}
                <span className="text-gray-900 dark:text-white truncate">
                  {entry.name}
                </span>
              </div>
              <span className="text-gray-500 dark:text-gray-400 text-sm">
                {entry.type === 'file' ? formatSize(entry.size) : '-'}
              </span>
              <span className="text-gray-500 dark:text-gray-400 text-sm">
                {formatDate(entry.modified)}
              </span>
            </button>
          ))}
        </div>
      </div>
      
      {/* File Preview */}
      {selectedFile && (
        <div className="w-1/2 border-l border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 flex flex-col">
          <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white">
                {selectedFile.name}
              </h3>
              <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400 mt-1">
                <span className="flex items-center gap-1">
                  <HardDrive className="w-4 h-4" />
                  {formatSize(selectedFile.size)}
                </span>
                <span className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  {formatDate(selectedFile.modified)}
                </span>
              </div>
            </div>
            <button
              onClick={() => setSelectedFile(null)}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded"
            >
              ×
            </button>
          </div>
          
          <div className="flex-1 overflow-auto p-4">
            {selectedFile.contentType === 'markdown' ? (
              <div 
                className="prose dark:prose-invert max-w-none"
                dangerouslySetInnerHTML={{ __html: marked(selectedFile.content) }}
              />
            ) : selectedFile.contentType === 'json' ? (
              <pre className="text-sm text-gray-800 dark:text-gray-200 font-mono whitespace-pre-wrap">
                {JSON.stringify(JSON.parse(selectedFile.content), null, 2)}
              </pre>
            ) : (
              <pre className="text-sm text-gray-800 dark:text-gray-200 font-mono whitespace-pre-wrap">
                {selectedFile.content}
              </pre>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
