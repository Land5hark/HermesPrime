---
name: youtube-transcript
description: Automatically fetch YouTube video transcripts when a YouTube URL is shared. Saves transcripts to reference files for later retrieval and context building. Use when the user shares a YouTube link and wants you to understand the content, extract key information, or reference it later.
metadata:
  clawdbot:
    emoji: "📺"
    tags: ["youtube", "transcript", "video", "research", "content-extraction"]
    category: research
---

# YouTube Transcript Skill

## What This Skill Does

Automatically processes YouTube URLs shared by the user:
1. Detects YouTube links in messages
2. Fetches video metadata (title, channel, duration)
3. Extracts transcript (captions/subtitles)
4. Saves to organized reference files
5. Provides summary for immediate context

## Usage

**Automatic:** When you paste a YouTube URL, I'll fetch the transcript and save it.

**Manual:** 
> "Get the transcript for [YouTube URL]"
> "Summarize this video: [YouTube URL]"
> "Save this YouTube video for reference"

## Output

**Files created:**
- `references/youtube/YYYY-MM-DD-video-title.md` — Full transcript with metadata
- `references/youtube/index.md` — Master index of all saved videos

**Immediate response:**
- Video title and channel
- Duration and key topics
- Brief summary (3-5 bullet points)
- File location for reference

## Features

- Auto-detects YouTube URLs (youtube.com, youtu.be)
- Handles videos with/without captions
- Falls back to audio transcription if needed
- Organizes by date for easy retrieval
- Cross-references with memory search
- Links related videos by topic

## Example

**You:** https://www.youtube.com/watch?v=O1ICQworLVc

**I respond:**
```
📺 Video saved: "Title Here" by Channel Name (15:32)

Key points:
• Main concept explained
• Technical approach shown
• Tools/resources mentioned

Full transcript: references/youtube/2026-02-16-title-here.md
```

## Retrieval

**Find saved videos:**
> "Show me my saved YouTube videos"
> "Find that video about [topic]"
> "What was in the genome analysis video?"

**Search transcripts:**
> "Search my YouTube references for [keyword]"

---

*Never lose context from shared videos again.*
