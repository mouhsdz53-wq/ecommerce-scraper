from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from loguru import logger
from scrapers.utils import get_headers, rate_limiter, scraper_cache, handle_scraping_error
import asyncio


class AmazonScraper:
    """Scraper pour Amazon - Bestsellers et produits"""
    
    def __init__(self):
        self.base_url = "https://www.amazon.com"
        self.headers = get_headers()
    
    async def scrape_bestsellers(self, category: str = "electronics", limit: int = 50) -> List[Dict]:
        """
        Scraper les bestsellers Amazon
        """
        cache_key = f"amazon_bestsellers_{category}"
        cached_data = scraper_cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        products = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent=self.headers["User-Agent"])
                page = await context.new_page()
                
                # URL des bestsellers
                url = f"{self.base_url}/Best-Sellers-{category}/zgbs/{category}"
                
                logger.info(f"Scraping Amazon bestsellers: {url}")
                rate_limiter.wait()
                
                await page.goto(url, wait_until="networkidle")
                await asyncio.sleep(2)  # Attendre le chargement complet
                
                # Extraire le HTML
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Parser les produits
                product_items = soup.find_all('div', {'class': 'zg-grid-general-faceout'})[:limit]
                
                for item in product_items:
                    try:
                        # Nom du produit
                        title_elem = item.find('div', {'class': '_cDEzb_p13n-sc-css-line-clamp-3_g3dy1'})
                        if not title_elem:
                            title_elem = item.find('a', {'class': 'a-link-normal'})
                        
                        title = title_elem.text.strip() if title_elem else "Unknown"
                        
                        # Prix
                        price_elem = item.find('span', {'class': 'a-price-whole'})
                        price = 0.0
                        if price_elem:
                            price_text = price_elem.text.replace(',', '').replace('$', '').strip()
                            try:
                                price = float(price_text)
                            except:
                                price = 0.0
                        
                        # URL
                        link_elem = item.find('a', {'class': 'a-link-normal'})
                        product_url = self.base_url + link_elem['href'] if link_elem and 'href' in link_elem.attrs else ""
                        
                        # ASIN
                        asin = ""
                        if '/dp/' in product_url:
                            asin = product_url.split('/dp/')[1].split('/')[0]
                        
                        # Image
                        img_elem = item.find('img')
                        image_url = img_elem['src'] if img_elem and 'src' in img_elem.attrs else ""
                        
                        # Rating
                        rating_elem = item.find('span', {'class': 'a-icon-alt'})
                        rating = 0.0
                        if rating_elem:
                            rating_text = rating_elem.text.split()[0]
                            try:
                                rating = float(rating_text)
                            except:
                                rating = 0.0
                        
                        # Reviews count
                        reviews_elem = item.find('span', {'class': 'a-size-small'})
                        reviews_count = 0
                        if reviews_elem:
                            reviews_text = reviews_elem.text.replace(',', '').strip()
                            try:
                                reviews_count = int(reviews_text)
                            except:
                                reviews_count = 0
                        
                        product = {
                            "nom": title,
                            "prix": price,
                            "url": product_url,
                            "source": "amazon",
                            "categorie": category,
                            "asin": asin,
                            "image_url": image_url,
                            "rating": rating,
                            "reviews_count": reviews_count,
                            "stock_status": "in_stock"
                        }
                        
                        products.append(product)
                        logger.info(f"Scraped Amazon product: {title[:50]}...")
                    
                    except Exception as e:
                        logger.error(f"Error parsing Amazon product: {str(e)}")
                        continue
                
                await browser.close()
                
                # Mettre en cache
                scraper_cache.set(cache_key, products)
                
                logger.info(f"Successfully scraped {len(products)} Amazon products")
                return products
        
        except Exception as e:
            error = handle_scraping_error(e, "amazon", url)
            return []
    
    async def scrape_product_details(self, asin: str) -> Optional[Dict]:
        """
        Scraper les détails d'un produit Amazon par ASIN
        """
        cache_key = f"amazon_product_{asin}"
        cached_data = scraper_cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent=self.headers["User-Agent"])
                page = await context.new_page()
                
                url = f"{self.base_url}/dp/{asin}"
                
                logger.info(f"Scraping Amazon product details: {url}")
                rate_limiter.wait()
                
                await page.goto(url, wait_until="networkidle")
                await asyncio.sleep(2)
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Extraire description
                description_elem = soup.find('div', {'id': 'feature-bullets'})
                description = description_elem.text.strip() if description_elem else ""
                
                # Extraire plus de détails si nécessaire
                
                await browser.close()
                
                product_details = {
                    "asin": asin,
                    "description": description,
                    "url": url
                }
                
                scraper_cache.set(cache_key, product_details)
                
                return product_details
        
        except Exception as e:
            handle_scraping_error(e, "amazon", f"{self.base_url}/dp/{asin}")
            return None


# Instance globale
amazon_scraper = AmazonScraper()
