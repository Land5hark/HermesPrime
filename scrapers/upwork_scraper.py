#!/usr/bin/env python3
"""
Upwork Job Scraper
Scrapes job listings from Upwork and outputs to JSON/CSV
Usage: python3 upwork_scraper.py --search "copywriting" --output jobs.json
"""

import argparse
import json
import csv
import sys
import re
from datetime import datetime
from urllib.parse import urlencode, quote
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

class UpworkScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.jobs = []
        
    def build_search_url(self, query, category=None, sort_by="recency"):
        """Build Upwork search URL"""
        base_url = "https://www.upwork.com/nx/jobs/search/"
        params = {
            "q": query,
            "sort": sort_by
        }
        if category:
            params["category"] = category
        return f"{base_url}?{urlencode(params)}"
    
    def parse_job_card(self, card_html):
        """Extract job details from a job card HTML"""
        soup = BeautifulSoup(card_html, 'html.parser')
        job = {}
        
        try:
            # Job title
            title_elem = soup.find('h2') or soup.find('a', {'data-test': 'job-title'})
            if title_elem:
                job['title'] = title_elem.get_text(strip=True)
                job['url'] = title_elem.get('href', '')
                if job['url'] and not job['url'].startswith('http'):
                    job['url'] = f"https://www.upwork.com{job['url']}"
            
            # Description snippet
            desc_elem = soup.find('div', {'data-test': 'job-description'}) or \
                       soup.find('p', class_=re.compile('description', re.I))
            if desc_elem:
                job['description'] = desc_elem.get_text(strip=True)
            
            # Budget/Rate
            budget_elem = soup.find('span', {'data-test': 'budget'}) or \
                         soup.find('strong', string=re.compile('\$'))
            if budget_elem:
                job['budget'] = budget_elem.get_text(strip=True)
            
            # Posted time
            time_elem = soup.find('span', {'data-test': 'posted-on'}) or \
                       soup.find('small', string=re.compile('ago|hour|day', re.I))
            if time_elem:
                job['posted'] = time_elem.get_text(strip=True)
            
            # Client info
            client_elem = soup.find('span', {'data-test': 'client-info'}) or \
                         soup.find('a', href=re.compile('/clients/'))
            if client_elem:
                job['client'] = client_elem.get_text(strip=True)
            
            # Skills/tags
            skills = []
            skill_elems = soup.find_all('span', {'data-test': 'skill'}) or \
                         soup.find_all('a', class_=re.compile('skill', re.I))
            for skill in skill_elems:
                skills.append(skill.get_text(strip=True))
            job['skills'] = skills
            
            # Proposals count
            proposals_elem = soup.find('span', string=re.compile('proposals?', re.I))
            if proposals_elem:
                job['proposals'] = proposals_elem.get_text(strip=True)
            
        except Exception as e:
            print(f"Error parsing job card: {e}", file=sys.stderr)
            
        return job
    
    def scrape_jobs(self, query, max_jobs=50, scroll_pause=2):
        """Scrape jobs from Upwork"""
        url = self.build_search_url(query)
        print(f"Scraping: {url}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()
            
            try:
                page.goto(url, wait_until='networkidle', timeout=60000)
                time.sleep(3)  # Wait for dynamic content
                
                # Scroll to load more jobs
                last_height = page.evaluate('document.body.scrollHeight')
                jobs_loaded = 0
                
                while jobs_loaded < max_jobs:
                    # Get current job cards
                    content = page.content()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Find job cards - Upwork uses various selectors
                    job_cards = soup.find_all('article', {'data-test': 'job-tile'}) or \
                               soup.find_all('div', class_=re.compile('job-tile|air-card', re.I)) or \
                               soup.find_all('section', class_=re.compile('job', re.I))
                    
                    print(f"Found {len(job_cards)} job cards on current page")
                    
                    for card in job_cards[jobs_loaded:]:
                        job = self.parse_job_card(str(card))
                        if job and job.get('title'):
                            job['scraped_at'] = datetime.now().isoformat()
                            job['search_query'] = query
                            self.jobs.append(job)
                            jobs_loaded += 1
                            print(f"  [{jobs_loaded}] {job.get('title', 'No title')[:60]}...")
                            
                        if jobs_loaded >= max_jobs:
                            break
                    
                    if jobs_loaded >= max_jobs:
                        break
                    
                    # Scroll down
                    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    time.sleep(scroll_pause)
                    
                    new_height = page.evaluate('document.body.scrollHeight')
                    if new_height == last_height:
                        print("Reached end of page")
                        break
                    last_height = new_height
                    
            except Exception as e:
                print(f"Error during scraping: {e}", file=sys.stderr)
                
            finally:
                browser.close()
        
        return self.jobs
    
    def save_json(self, filename):
        """Save jobs to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(self.jobs)} jobs to {filename}")
    
    def save_csv(self, filename):
        """Save jobs to CSV file"""
        if not self.jobs:
            print("No jobs to save")
            return
        
        # Flatten skills list for CSV
        jobs_for_csv = []
        for job in self.jobs:
            job_copy = job.copy()
            job_copy['skills'] = ', '.join(job.get('skills', []))
            jobs_for_csv.append(job_copy)
        
        # Get all possible fields
        fieldnames = set()
        for job in jobs_for_csv:
            fieldnames.update(job.keys())
        fieldnames = sorted(fieldnames)
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(jobs_for_csv)
        print(f"Saved {len(self.jobs)} jobs to {filename}")
    
    def filter_jobs(self, min_budget=None, max_proposals=None, exclude_terms=None):
        """Filter jobs based on criteria"""
        filtered = []
        exclude_terms = exclude_terms or []
        
        for job in self.jobs:
            # Check exclude terms
            title_desc = f"{job.get('title', '')} {job.get('description', '')}".lower()
            if any(term.lower() in title_desc for term in exclude_terms):
                continue
            
            # Check budget (basic parsing)
            if min_budget and job.get('budget'):
                budget_str = job['budget'].replace('$', '').replace(',', '').replace('/hr', '').replace('Fixed Price: ', '')
                try:
                    budget_val = float(re.findall(r'[\d.]+', budget_str)[0])
                    if budget_val < min_budget:
                        continue
                except:
                    pass
            
            # Check proposals
            if max_proposals and job.get('proposals'):
                try:
                    prop_num = int(re.findall(r'\d+', job['proposals'])[0])
                    if prop_num > max_proposals:
                        continue
                except:
                    pass
            
            filtered.append(job)
        
        self.jobs = filtered
        return filtered


def main():
    parser = argparse.ArgumentParser(description='Scrape Upwork job listings')
    parser.add_argument('--search', '-s', required=True, help='Search query')
    parser.add_argument('--max', '-m', type=int, default=50, help='Maximum jobs to scrape (default: 50)')
    parser.add_argument('--output', '-o', default='upwork_jobs.json', help='Output file (json or csv)')
    parser.add_argument('--visible', '-v', action='store_true', help='Show browser window (not headless)')
    parser.add_argument('--min-budget', type=float, help='Minimum budget filter')
    parser.add_argument('--max-proposals', type=int, help='Maximum proposals filter')
    parser.add_argument('--exclude', nargs='+', help='Terms to exclude from results')
    
    args = parser.parse_args()
    
    scraper = UpworkScraper(headless=not args.visible)
    jobs = scraper.scrape_jobs(args.search, max_jobs=args.max)
    
    if jobs:
        # Apply filters
        scraper.filter_jobs(
            min_budget=args.min_budget,
            max_proposals=args.max_proposals,
            exclude_terms=args.exclude
        )
        
        # Save results
        if args.output.endswith('.csv'):
            scraper.save_csv(args.output)
        else:
            scraper.save_json(args.output)
        
        print(f"\nTotal jobs found: {len(jobs)}")
        print(f"Filtered jobs: {len(scraper.jobs)}")
    else:
        print("No jobs found")
        sys.exit(1)


if __name__ == '__main__':
    main()
