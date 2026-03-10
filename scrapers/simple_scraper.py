#!/usr/bin/env python3
"""
Simple Upwork Job Scraper using ScrapingAnt API
Free tier: 10,000 API credits
"""

import argparse
import json
import csv
import sys
import re
from urllib.parse import urlencode, quote
from datetime import datetime
import requests

class SimpleUpworkScraper:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.jobs = []
        self.base_url = "https://api.scrapingant.com/v2/general"
        
    def fetch_page(self, url):
        """Fetch page using ScrapingAnt API"""
        if self.api_key:
            # Use ScrapingAnt with API key
            params = {
                'url': url,
                'x-api-key': self.api_key,
                'browser': 'true',
                'wait_for_selector': 'article',
                'wait_for_timeout': '5000'
            }
            api_url = f"{self.base_url}?{urlencode(params)}"
        else:
            # Try direct fetch (will likely be blocked but worth trying)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            try:
                response = requests.get(url, headers=headers, timeout=30)
                return response.text
            except:
                return None
        
        try:
            response = requests.get(api_url, timeout=120)
            if response.status_code == 200:
                return response.text
            else:
                print(f"API error: {response.status_code} - {response.text[:200]}")
                return None
        except Exception as e:
            print(f"Request error: {e}")
            return None
    
    def parse_jobs_from_html(self, html):
        """Parse job listings from HTML"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []
        
        # Save HTML for debugging
        with open('/home/clawd/scraper_debug.html', 'w', encoding='utf-8') as f:
            f.write(html[:50000])  # First 50k chars
        
        # Find job cards - try multiple selectors
        job_cards = soup.find_all('article', {'data-test': 'job-tile'})
        if not job_cards:
            job_cards = soup.find_all('article')
        if not job_cards:
            job_cards = soup.find_all('div', class_=re.compile('job-tile|air-card', re.I))
        if not job_cards:
            job_cards = soup.find_all('section', class_=re.compile('job', re.I))
        
        print(f"Found {len(job_cards)} job cards")
        
        for card in job_cards:
            job = {}
            try:
                # Title
                title = card.find('h2') or card.find('a', {'data-test': 'job-title'})
                if title:
                    job['title'] = title.get_text(strip=True)
                    href = title.get('href', '')
                    if href:
                        job['url'] = f"https://www.upwork.com{href}" if not href.startswith('http') else href
                
                # Description
                desc = card.find('div', {'data-test': 'job-description'}) or card.find('p')
                if desc:
                    job['description'] = desc.get_text(strip=True)[:300]
                
                # Budget
                budget = card.find('span', {'data-test': 'budget'}) or card.find(string=re.compile('\$'))
                if budget:
                    if hasattr(budget, 'get_text'):
                        job['budget'] = budget.get_text(strip=True)
                    else:
                        job['budget'] = str(budget).strip()
                
                # Posted time
                posted = card.find('span', {'data-test': 'posted-on'}) or card.find('small')
                if posted:
                    job['posted'] = posted.get_text(strip=True)
                
                # Skills
                skills = []
                for skill in card.find_all('span', {'data-test': 'skill'}):
                    skills.append(skill.get_text(strip=True))
                job['skills'] = skills
                
                if job.get('title'):
                    job['scraped_at'] = datetime.now().isoformat()
                    jobs.append(job)
                    
            except Exception as e:
                print(f"Parse error: {e}")
                continue
        
        return jobs
    
    def scrape(self, query, max_jobs=30):
        """Scrape jobs from Upwork"""
        search_url = f"https://www.upwork.com/nx/jobs/search/?q={quote(query)}&sort=recency"
        print(f"Fetching: {search_url}")
        
        html = self.fetch_page(search_url)
        if not html:
            print("Failed to fetch page. Upwork may be blocking requests.")
            print("\nOptions:")
            print("1. Use ScrapingAnt API (free 10k credits): https://scrapingant.com")
            print("2. Use Bright Data API: https://brightdata.com")
            print("3. Install Chrome/Chromium with: sudo apt install chromium-browser")
            return []
        
        jobs = self.parse_jobs_from_html(html)
        print(f"\nParsed {len(jobs)} jobs")
        return jobs[:max_jobs]
    
    def save(self, jobs, filename):
        """Save jobs to file"""
        if filename.endswith('.csv'):
            self._save_csv(jobs, filename)
        else:
            self._save_json(jobs, filename)
    
    def _save_json(self, jobs, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(jobs)} jobs to {filename}")
    
    def _save_csv(self, jobs, filename):
        if not jobs:
            return
        fieldnames = set()
        for job in jobs:
            fieldnames.update(job.keys())
        fieldnames = sorted(fieldnames)
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for job in jobs:
                row = job.copy()
                if 'skills' in row:
                    row['skills'] = ', '.join(row['skills'])
                writer.writerow(row)
        print(f"Saved {len(jobs)} jobs to {filename}")


def main():
    parser = argparse.ArgumentParser(description='Simple Upwork scraper')
    parser.add_argument('--search', '-s', required=True, help='Search query')
    parser.add_argument('--max', '-m', type=int, default=30, help='Max jobs')
    parser.add_argument('--output', '-o', default='jobs.json', help='Output file')
    parser.add_argument('--api-key', '-k', help='ScrapingAnt API key')
    
    args = parser.parse_args()
    
    scraper = SimpleUpworkScraper(api_key=args.api_key)
    jobs = scraper.scrape(args.search, max_jobs=args.max)
    
    if jobs:
        for i, job in enumerate(jobs, 1):
            print(f"\n[{i}] {job.get('title', 'No title')}")
            print(f"    Budget: {job.get('budget', 'N/A')}")
            print(f"    Posted: {job.get('posted', 'N/A')}")
            if job.get('url'):
                print(f"    URL: {job['url']}")
        
        scraper.save(jobs, args.output)
    else:
        print("No jobs found")


if __name__ == '__main__':
    main()
