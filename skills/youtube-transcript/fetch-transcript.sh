#!/bin/bash
# YouTube Transcript Fetcher
# Usage: ./fetch-transcript.sh <youtube-url> [output-dir]

URL="$1"
OUTPUT_DIR="${2:-references/youtube}"

if [ -z "$URL" ]; then
    echo "Usage: $0 <youtube-url> [output-dir]"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Fetch metadata and transcript using yt-dlp
# Note: yt-dlp must be installed

VIDEO_ID=$(echo "$URL" | sed -n 's/.*[?&]v=\([^&]*\).*/\1/p; s/.*youtu\.be\/\([^?]*\).*/\1/p')

if [ -z "$VIDEO_ID" ]; then
    echo "Error: Could not extract video ID from URL"
    exit 1
fi

echo "Fetching transcript for video ID: $VIDEO_ID"

# Get video info
yt-dlp --dump-json --skip-download "$URL" 2>/dev/null > /tmp/video_info.json

if [ ! -f /tmp/video_info.json ]; then
    echo "Error: Could not fetch video info. Is yt-dlp installed?"
    exit 1
fi

# Extract metadata
TITLE=$(cat /tmp/video_info.json | grep -o '"title": "[^"]*"' | head -1 | cut -d'"' -f4)
CHANNEL=$(cat /tmp/video_info.json | grep -o '"channel": "[^"]*"' | head -1 | cut -d'"' -f4)
DURATION=$(cat /tmp/video_info.json | grep -o '"duration": [0-9]*' | head -1 | grep -o '[0-9]*')
UPLOAD_DATE=$(cat /tmp/video_info.json | grep -o '"upload_date": "[^"]*"' | head -1 | cut -d'"' -f4)

# Format duration
if [ -n "$DURATION" ]; then
    MINUTES=$((DURATION / 60))
    SECONDS=$((DURATION % 60))
    DURATION_FMT="${MINUTES}:$(printf '%02d' $SECONDS)"
else
    DURATION_FMT="unknown"
fi

# Create safe filename
SAFE_TITLE=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//' | cut -c1-50)
TODAY=$(date +%Y-%m-%d)
FILENAME="${TODAY}-${SAFE_TITLE}.md"
OUTPUT_FILE="$OUTPUT_DIR/$FILENAME"

# Try to get transcript
echo "Attempting to download transcript..."
yt-dlp --write-sub --write-auto-sub --sub-langs en --skip-download --output "/tmp/%(id)s" "$URL" 2>/dev/null

# Find the subtitle file
SUBFILE=$(ls /tmp/${VIDEO_ID}*.en*.vtt 2>/dev/null | head -1)

if [ -f "$SUBFILE" ]; then
    # Convert VTT to clean text
    cat "$SUBFILE" | sed 's/<[^>]*>//g' | grep -v '^[0-9][0-9]:' | grep -v '^$' | sed 's/^WEBVTT$//' | sed '/^$/d' > /tmp/clean_transcript.txt
    TRANSCRIPT_AVAILABLE="Yes (auto-generated or captions)"
else
    TRANSCRIPT_AVAILABLE="No (video has no captions)"
fi

# Create markdown file
cat > "$OUTPUT_FILE" << EOF
# YouTube Video Reference

**Title:** $TITLE  
**Channel:** $CHANNEL  
**Duration:** $DURATION_FMT  
**Upload Date:** ${UPLOAD_DATE:0:4}-${UPLOAD_DATE:4:2}-${UPLOAD_DATE:6:2}  
**URL:** $URL  
**Video ID:** $VIDEO_ID  
**Transcript Available:** $TRANSCRIPT_AVAILABLE  
**Saved Date:** $TODAY  

---

## Summary

[To be filled with key points from video]

---

## Transcript

EOF

if [ -f /tmp/clean_transcript.txt ]; then
    cat /tmp/clean_transcript.txt >> "$OUTPUT_FILE"
    rm /tmp/clean_transcript.txt
else
    echo "*No transcript available for this video.*" >> "$OUTPUT_FILE"
fi

# Clean up
rm -f /tmp/video_info.json /tmp/${VIDEO_ID}*.vtt /tmp/${VIDEO_ID}*.srt 2>/dev/null

echo "Saved to: $OUTPUT_FILE"
