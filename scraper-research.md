# Upwork/Fiverr Scrapers - Research Results

## GITHUB OPEN SOURCE SCRAPERS (FREE)

### UPWORK SCRAPERS

**1. Upwork Job Scraper + Webhook (Chrome Extension)**
- **URL:** https://github.com/richardadonnell/Upwork-Job-Scraper
- **Chrome Store:** https://chromewebstore.google.com/detail/upwork-job-scraper-+-webh/mojpfejnpifdgjjknalhghclnaifnjkg
- **What it does:**
  - Scrapes job listings from Upwork automatically
  - Sends jobs to webhook URL (Discord, Slack, Zapier, etc.)
  - Customizable check frequency (days/hours/minutes)
  - Browser notifications for new jobs
  - Job deduplication (no duplicates)
  - Badge notifications on extension icon
  - Master toggle on/off
  - Manual scrape button
- **Best for:** Real-time job alerts without coding
- **Status:** Active development (updated Nov 2025)
- **Limitations:** Chrome extension only, may break if Upwork changes site

**2. Upwork Job Scraper Ecosystem (AWS Lambda)**
- **URL:** https://github.com/asaniczka/Upwork-Job-Scraper
- **What it does:**
  - Microservices architecture (Lambda functions)
  - Authenticator Lambda: Manages Upwork API tokens
  - Job Fetcher Lambda: Extracts ALL jobs (~6,000/day)
  - Data Enrichment Service: Adds client statistics
  - PostgreSQL database for storage
  - Cost-efficient design
- **Best for:** Large-scale scraping, archiving all jobs
- **Status:** Production-ready
- **Limitations:** Requires AWS setup, technical knowledge needed

**3. Upwork Job Scraper (Python/Playwright)**
- **URL:** https://github.com/calebmwelsh/Upwork-Job-Scraper
- **What it does:**
  - Playwright-based automation
  - Saves to CSV or JSON
  - Should've just given me an API key (dev humor)
- **Best for:** Custom Python automation

**4. Upwork Job Scraper (Python CLI)**
- **URL:** https://github.com/sudhamjayanthi/upwork-job-scraper
- **What it does:**
  - Terminal-based job browsing
  - Check jobs from command line
- **Best for:** CLI enthusiasts

**5. Upwork Job Scraper (Go)**
- **URL:** https://github.com/hashiromer/Upwork-Jobs-scraper-
- **What it does:**
  - Go-based scraper
  - Fetches new jobs
- **Best for:** Go developers, speed

**6. Upwork Scraper (Python/Jupyter)**
- **URL:** https://github.com/gasparian/upwork_parsing
- **What it does:**
  - Jupyter notebook for parsing
  - Data analysis focused
- **Best for:** Data analysis, research

### FIVERR SCRAPERS

**1. Fiverr Scraper (Python)**
- **URL:** https://github.com/Lazar-T/fiverr_scraper
- **What it does:**
  - Scrapes individual Fiverr profiles
  - Uses requests, lxml, termcolor
  - Simple CLI interface
- **Best for:** Profile research
- **Status:** Older (2017), may need updates

**2. Fiverr Gig Scraper**
- **URL:** https://github.com/omar-elmaria/fiverr_scraper
- **What it does:**
  - Crawls gig information from Data Processing category
  - Python script
- **Best for:** Category-specific scraping

**3. Fiverr Scraper Extension**
- **URL:** https://github.com/misbahmunir355/FiverrGigsScraper_extension
- **What it does:**
  - Browser extension for scraping Fiverr
- **Best for:** Browser-based scraping

---

## COMMERCIAL SCRAPING APIs (PAID)

### 1. BRIGHT DATA (Formerly Luminati)
- **URL:** https://brightdata.com/products/web-scraper
- **Pricing:** 
  - Pay-as-you-go: $1.50 per 1K records
  - $499/month: 510K records ($0.98 per 1K)
  - $999/month: 1M records ($0.83 per 1K)
- **Features:**
  - 437+ ready-made scrapers
  - 150M+ residential proxies
  - Automatic IP rotation
  - CAPTCHA solving
  - JavaScript rendering
  - No-code options
  - 99.99% uptime
- **Best for:** Enterprise, scale, reliability
- **Free trial:** Yes

### 2. SCRAPINGBEE
- **URL:** https://www.scrapingbee.com
- **Pricing:**
  - Free: 1,000 API calls
  - Startup: $49/month (500K credits)
  - Business: $249/month (3M credits)
- **Features:**
  - Proxy rotation
  - JavaScript rendering
  - Google Sheets integration
  - No-code web scraping
- **Best for:** Developers who need simple API

### 3. SCRAPINGANT
- **URL:** https://scrapingant.com
- **Pricing:**
  - Free: 10,000 API credits
  - Enthusiast: $19/month (100K credits)
  - Startup: $49/month (500K credits)
  - Business: $249/month (3M credits)
- **Features:**
  - Unlimited concurrency
  - 99.99% uptime
  - 85.5% anti-scraping avoidance
  - Custom cloud browser
- **Best for:** Budget-conscious, high volume

### 4. SCRAPERAPI
- **URL:** https://www.scraperapi.com
- **Pricing:**
  - Free: 5,000 API credits
  - Paid plans start at $49/month
- **Features:**
  - 40M+ proxies
  - 50+ countries
  - Structured data endpoints (Amazon, Google, etc.)
  - Async scraper service
  - DataPipeline (no-code)
  - LangChain integration
- **Best for:** Structured data extraction

---

## APIFY ACTORS (SERVERLESS SCRAPERS)

Apify Store has 18,000+ scrapers but **NO specific Upwork/Fiverr actors found** in search.
However, you can:
1. Use generic **Website Content Crawler** to scrape any site
2. Build custom actor for Upwork/Fiverr
3. Use **Python + Scrapy** on Apify platform

---

## RECOMMENDATIONS

### FOR IMMEDIATE USE (No Budget)
1. **Install Chrome Extension:** https://chromewebstore.google.com/detail/upwork-job-scraper-+-webh/mojpfejnpifdgjjknalhghclnaifnjkg
   - Set webhook to Discord or Zapier
   - Get real-time alerts
   - Free forever

2. **Use GitHub Python Scraper:**
   ```bash
   git clone https://github.com/richardadonnell/Upwork-Job-Scraper
   cd Upwork-Job-Scraper
   # Modify for your needs
   ```

### FOR SCALE (With Budget)
1. **Bright Data** - Most reliable, 437+ scrapers
2. **ScraperAPI** - Best for structured data
3. **ScrapingAnt** - Best value for money

### FOR CUSTOM SOLUTION
Build on **Apify** using their Python template:
- Free tier: 10 compute hours/month
- Pay-as-you-go after
- Can schedule runs
- Export to JSON/CSV/API

---

## SETUP FOR YOUR USE CASE

### What You Need:
1. Scrape Upwork jobs matching your criteria
2. Filter for quick-turnaround, low-competition jobs
3. Get alerts in real-time
4. Maybe auto-apply or auto-draft proposals

### Best Stack:
1. **Chrome Extension** (immediate alerts)
2. **Zapier** (connect to Google Sheets/Discord)
3. **Custom filter** (only high-value jobs)
4. **AI proposal drafter** (I can help with this)

### Cost:
- $0 to start (Chrome extension + webhook)
- $20-50/month if you scale (ScrapingAnt or similar)

---

## LEGAL NOTE

Upwork and Fiverr ToS generally prohibit scraping. However:
- **Browser extensions** operating as "user assistance" tools are usually tolerated
- **API-based scraping** is higher risk
- **Personal use** (finding jobs for yourself) is lower risk than commercial resale

Use at your own risk. Consider using official APIs if available.
