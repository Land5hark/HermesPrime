#!/usr/bin/env python3
"""
Job Monitor - Scrape and alert on new jobs
Compares against previous run to find new listings
Usage: python3 job_monitor.py --search "copywriting" --webhook YOUR_WEBHOOK_URL
"""

import argparse
import json
import os
import sys
from datetime import datetime
import requests
from upwork_scraper import UpworkScraper

class JobMonitor:
    def __init__(self, search_query, state_file="monitor_state.json"):
        self.search_query = search_query
        self.state_file = state_file
        self.seen_jobs = self.load_state()
        
    def load_state(self):
        """Load previously seen job IDs"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return set(json.load(f))
        return set()
    
    def save_state(self):
        """Save seen job IDs"""
        with open(self.state_file, 'w') as f:
            json.dump(list(self.seen_jobs), f)
    
    def get_job_id(self, job):
        """Generate unique ID for a job"""
        # Use URL or title as ID
        return job.get('url', '') or job.get('title', '')
    
    def find_new_jobs(self, jobs):
        """Find jobs not seen before"""
        new_jobs = []
        for job in jobs:
            job_id = self.get_job_id(job)
            if job_id and job_id not in self.seen_jobs:
                new_jobs.append(job)
                self.seen_jobs.add(job_id)
        return new_jobs
    
    def format_discord_message(self, job):
        """Format job for Discord webhook"""
        title = job.get('title', 'New Job')[:100]
        budget = job.get('budget', 'Not specified')
        posted = job.get('posted', 'Recently')
        url = job.get('url', '')
        
        description = job.get('description', '')[:200]
        if len(job.get('description', '')) > 200:
            description += '...'
        
        return {
            "embeds": [{
                "title": title,
                "url": url,
                "color": 3447003,
                "fields": [
                    {"name": "Budget", "value": budget, "inline": True},
                    {"name": "Posted", "value": posted, "inline": True},
                    {"name": "Description", "value": description or "No description", "inline": False}
                ],
                "footer": {"text": f"Search: {self.search_query}"},
                "timestamp": datetime.now().isoformat()
            }]
        }
    
    def send_discord_alert(self, webhook_url, job):
        """Send job alert to Discord"""
        try:
            payload = self.format_discord_message(job)
            response = requests.post(webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception as e:
            print(f"Failed to send Discord alert: {e}")
            return False
    
    def send_console_alert(self, job):
        """Print job alert to console"""
        print("\n" + "="*60)
        print(f"🚨 NEW JOB: {job.get('title', 'Unknown')}")
        print(f"💰 Budget: {job.get('budget', 'Not specified')}")
        print(f"⏰ Posted: {job.get('posted', 'Recently')}")
        print(f"🔗 URL: {job.get('url', 'No URL')}")
        if job.get('description'):
            desc = job['description'][:150] + '...' if len(job['description']) > 150 else job['description']
            print(f"📝 Description: {desc}")
        print("="*60)
    
    def run(self, max_jobs=30, webhook_url=None, min_budget=None, max_proposals=None):
        """Run monitor cycle"""
        print(f"[{datetime.now()}] Checking for new jobs: '{self.search_query}'")
        
        # Scrape jobs
        scraper = UpworkScraper(headless=True)
        jobs = scraper.scrape_jobs(self.search_query, max_jobs=max_jobs)
        
        if not jobs:
            print("No jobs found")
            return []
        
        # Apply filters
        jobs = scraper.filter_jobs(
            min_budget=min_budget,
            max_proposals=max_proposals
        )
        
        # Find new jobs
        new_jobs = self.find_new_jobs(jobs)
        
        if new_jobs:
            print(f"\n🎉 Found {len(new_jobs)} NEW jobs!")
            
            for job in new_jobs:
                self.send_console_alert(job)
                
                if webhook_url:
                    if self.send_discord_alert(webhook_url, job):
                        print(f"  ✓ Discord alert sent")
                    else:
                        print(f"  ✗ Discord alert failed")
        else:
            print(f"No new jobs (checked {len(jobs)} total)")
        
        # Save state
        self.save_state()
        
        return new_jobs


def main():
    parser = argparse.ArgumentParser(description='Monitor Upwork for new jobs')
    parser.add_argument('--search', '-s', required=True, help='Search query')
    parser.add_argument('--webhook', '-w', help='Discord webhook URL for alerts')
    parser.add_argument('--max', '-m', type=int, default=30, help='Max jobs to check')
    parser.add_argument('--min-budget', type=float, help='Minimum budget')
    parser.add_argument('--max-proposals', type=int, help='Maximum proposals')
    parser.add_argument('--interval', '-i', type=int, help='Run every N minutes (loop mode)')
    parser.add_argument('--state', default='monitor_state.json', help='State file path')
    
    args = parser.parse_args()
    
    monitor = JobMonitor(args.search, state_file=args.state)
    
    if args.interval:
        # Loop mode
        print(f"Monitor running every {args.interval} minutes. Press Ctrl+C to stop.")
        try:
            while True:
                monitor.run(
                    max_jobs=args.max,
                    webhook_url=args.webhook,
                    min_budget=args.min_budget,
                    max_proposals=args.max_proposals
                )
                print(f"\nSleeping for {args.interval} minutes...\n")
                import time
                time.sleep(args.interval * 60)
        except KeyboardInterrupt:
            print("\nMonitor stopped")
    else:
        # Single run
        monitor.run(
            max_jobs=args.max,
            webhook_url=args.webhook,
            min_budget=args.min_budget,
            max_proposals=args.max_proposals
        )


if __name__ == '__main__':
    main()
