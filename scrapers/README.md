# Upwork & Fiverr Scrapers

Fast money scrapers for freelance job listings.

## Quick Start

### Upwork Scraper
```bash
# Basic usage
python3 upwork_scraper.py --search "email marketing" --output jobs.json

# With filters (recommended)
python3 upwork_scraper.py \
    --search "copywriting" \
    --max 50 \
    --min-budget 50 \
    --max-proposals 20 \
    --output jobs.json

# Quick run script
./scrape_upwork.sh "email copywriting"
```

### Fiverr Scraper
```bash
# Basic usage
python3 fiverr_scraper.py --search "copywriting" --output gigs.json

# With visible browser (debugging)
python3 fiverr_scraper.py --search "email marketing" --visible
```

## Command Options

### Upwork Scraper
| Option | Description |
|--------|-------------|
| `--search, -s` | Search query (required) |
| `--max, -m` | Max jobs to scrape (default: 50) |
| `--output, -o` | Output file (.json or .csv) |
| `--visible, -v` | Show browser window |
| `--min-budget` | Minimum budget filter |
| `--max-proposals` | Maximum proposals filter |
| `--exclude` | Terms to exclude (space-separated) |

### Fiverr Scraper
| Option | Description |
|--------|-------------|
| `--search, -s` | Search query (required) |
| `--max, -m` | Max gigs to scrape (default: 50) |
| `--output, -o` | Output file (.json or .csv) |
| `--visible, -v` | Show browser window |

## High-Value Search Queries

### Quick Turnaround / Urgent
```bash
python3 upwork_scraper.py --search "urgent copywriting" --max 30
python3 upwork_scraper.py --search "needed today email" --max 30
python3 upwork_scraper.py --search "quick turnaround" --max 30
```

### Specific Skills
```bash
python3 upwork_scraper.py --search "email sequence" --min-budget 100
python3 upwork_scraper.py --search "sales copy" --min-budget 150
python3 upwork_scraper.py --search "product descriptions bulk"
```

### Low Competition
```bash
python3 upwork_scraper.py --search "data cleanup" --max-proposals 10
python3 upwork_scraper.py --search "spreadsheet" --max-proposals 5
python3 upwork_scraper.py --search "transcription" --max-proposals 10
```

## Automation

### Cron Job (Every Hour)
```bash
# Add to crontab
crontab -e

# Add this line to run every hour
0 * * * * cd /home/clawd/.openclaw/workspace/scrapers && python3 upwork_scraper.py --search "email copywriting" --output /home/clawd/jobs_$(date +\%Y\%m\%d_\%H\%M).json >> /home/clawd/scraper.log 2>&1
```

### Continuous Monitor
```bash
# Run every 10 minutes
while true; do
    python3 upwork_scraper.py --search "copywriting" --output jobs_latest.json
    sleep 600
done
```

## Output Format

### JSON
```json
[
  {
    "title": "Email Marketing Sequence Needed",
    "description": "Looking for 5-email welcome series...",
    "budget": "$200-$400",
    "posted": "2 hours ago",
    "url": "https://www.upwork.com/jobs/...",
    "skills": ["Email Marketing", "Copywriting"],
    "scraped_at": "2024-01-15T10:30:00"
  }
]
```

### CSV
Opens in Excel/Google Sheets with columns:
- title
- description
- budget
- posted
- url
- skills
- proposals
- scraped_at

## Tips

1. **Run frequently** - Best jobs get claimed fast
2. **Use filters** - Avoid "expert only" or "agency" jobs
3. **Check proposals** - < 10 proposals = higher chance
4. **Sort by recency** - Scraper already does this
5. **Apply fast** - Have proposals ready to customize

## Troubleshooting

### Browser not launching
```bash
playwright install chromium
```

### Empty results
- Upwork may have changed their HTML structure
- Try `--visible` flag to see what's happening
- Check internet connection

### Blocked / CAPTCHA
- Upwork blocks aggressive scraping
- Use `--max 20` to limit requests
- Add delays between runs (10+ minutes)
- Use residential proxy if available

## Legal Note

These scrapers are for personal use only. Respect Upwork/Fiverr ToS:
- Don't resell scraped data
- Don't spam platforms
- Use reasonable request rates
- Consider official APIs when available

## Next Steps

1. **Set up alerts** - Send new jobs to Discord/Slack
2. **Auto-draft proposals** - Integrate with AI to draft responses
3. **Track success rate** - Log which jobs you win
4. **Build pipeline** - Scrape → Filter → Draft → Apply
