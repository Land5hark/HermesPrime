#!/usr/bin/env python3
"""
Fiverr Job/Gig Scraper
Scrapes buyer requests and gig listings from Fiverr
Usage: python3 fiverr_scraper.py --search "copywriting" --output gigs.json
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

class FiverrScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.gigs = []
        
    def build_search_url(self, query, category=None):
        """Build Fiverr search URL"""
        base_url = "https://www.fiverr.com/search/gigs"
        params = {
            "query": query,
            "source": "main_banner"
        }
        return f"{base_url}?{urlencode(params)}"
    
    def parse_gig_card(self, card_html):
        """Extract gig details from a gig card HTML"""
        soup = BeautifulSoup(card_html, 'html.parser')
        gig = {}
        
        try:
            # Gig title
            title_elem = soup.find('h3') or soup.find('a', class_=re.compile('gig-title', re.I))
            if title_elem:
                gig['title'] = title_elem.get_text(strip=True)
            
            # Seller name
            seller_elem = soup.find('a', class_=re.compile('seller-name', re.I)) or \
                         soup.find('span', class_=re.compile('seller', re.I))
            if seller_elem:
                gig['seller'] = seller_elem.get_text(strip=True)
            
            # Price
            price_elem = soup.find('span', class_=re.compile('price', re.I)) or \
                        soup.find('a', class_=re.compile('price', re.I))
            if price_elem:
                gig['price'] = price_elem.get_text(strip=True)
            
            # Rating
            rating_elem = soup.find('span', class_=re.compile('rating', re.I)) or \
                         soup.find('b', class_=re.compile('rating', re.I))
            if rating_elem:
                gig['rating'] = rating_elem.get_text(strip=True)
            
            # Reviews count
            reviews_elem = soup.find('span', string=re.compile('\(\d+\)'))
            if reviews_elem:
                gig['reviews'] = reviews_elem.get_text(strip=True)
            
            # Delivery time
            delivery_elem = soup.find('span', string=re.compile('\d+ day', re.I))
            if delivery_elem:
                gig['delivery'] = delivery_elem.get_text(strip=True)
            
            # Gig URL
            link_elem = soup.find('a', href=re.compile('/[^/]+/[^/]+'))
            if link_elem:
                href = link_elem.get('href', '')
                if href.startswith('/'):
                    gig['url'] = f"https://www.fiverr.com{href}"
                else:
                    gig['url'] = href
            
        except Exception as e:
            print(f"Error parsing gig card: {e}", file=sys.stderr)
            
        return gig
    
    def scrape_gigs(self, query, max_gigs=50, scroll_pause=2):
        """Scrape gigs from Fiverr search"""
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
                time.sleep(3)
                
                # Handle cookie popup if present
                try:
                    cookie_btn = page.locator('button:has-text("Accept")').first
                    if cookie_btn.is_visible(timeout=5000):
                        cookie_btn.click()
                        time.sleep(1)
                except:
                    pass
                
                # Scroll to load more gigs
                last_height = page.evaluate('document.body.scrollHeight')
                gigs_loaded = 0
                
                while gigs_loaded < max_gigs:
                    content = page.content()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Find gig cards - Fiverr uses various selectors
                    gig_cards = soup.find_all('div', class_=re.compile('gig-card|gig-wrapper', re.I)) or \
                               soup.find_all('article') or \
                               soup.find_all('div', {'data-test': 'gig-card'})
                    
                    print(f"Found {len(gig_cards)} gig cards on current page")
                    
                    for card in gig_cards[gigs_loaded:]:
                        gig = self.parse_gig_card(str(card))
                        if gig and gig.get('title'):
                            gig['scraped_at'] = datetime.now().isoformat()
                            gig['search_query'] = query
                            self.gigs.append(gig)
                            gigs_loaded += 1
                            print(f"  [{gigs_loaded}] {gig.get('title', 'No title')[:50]}...")
                            
                        if gigs_loaded >= max_gigs:
                            break
                    
                    if gigs_loaded >= max_gigs:
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
        
        return self.gigs
    
    def save_json(self, filename):
        """Save gigs to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.gigs, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(self.gigs)} gigs to {filename}")
    
    def save_csv(self, filename):
        """Save gigs to CSV file"""
        if not self.gigs:
            print("No gigs to save")
            return
        
        fieldnames = set()
        for gig in self.gigs:
            fieldnames.update(gig.keys())
        fieldnames = sorted(fieldnames)
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.gigs)
        print(f"Saved {len(self.gigs)} gigs to {filename}")


def main():
    parser = argparse.ArgumentParser(description='Scrape Fiverr gig listings')
    parser.add_argument('--search', '-s', required=True, help='Search query')
    parser.add_argument('--max', '-m', type=int, default=50, help='Maximum gigs to scrape (default: 50)')
    parser.add_argument('--output', '-o', default='fiverr_gigs.json', help='Output file (json or csv)')
    parser.add_argument('--visible', '-v', action='store_true', help='Show browser window (not headless)')
    
    args = parser.parse_args()
    
    scraper = FiverrScraper(headless=not args.visible)
    gigs = scraper.scrape_gigs(args.search, max_gigs=args.max)
    
    if gigs:
        if args.output.endswith('.csv'):
            scraper.save_csv(args.output)
        else:
            scraper.save_json(args.output)
        
        print(f"\nTotal gigs found: {len(gigs)}")
    else:
        print("No gigs found")
        sys.exit(1)


if __name__ == '__main__':
    main()
