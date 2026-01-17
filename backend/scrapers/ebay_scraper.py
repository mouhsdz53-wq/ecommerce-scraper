import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from loguru import logger
from scrapers.utils import get_headers, rate_limiter, scraper_cache, handle_scraping_error


class EbayScraper:
    """Scraper pour eBay - Sold items et trending searches"""
    
    def __init__(self):
        self.base_url = "https://www.ebay.com"
        self.headers = get_headers()
    
    async def scrape_sold_items(self, keyword: str, limit: int = 50) -> List[Dict]:
        """
        Scraper les articles vendus sur eBay
        """
        cache_key = f"ebay_sold_{keyword}"
        cached_data = scraper_cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        products = []
        
        try:
            async with httpx.AsyncClient(
                headers=self.headers, 
                timeout=30.0,
                follow_redirects=True
            ) as client:
                # URL pour articles vendus
                url = f"{self.base_url}/sch/i.html?_nkw={keyword}&LH_Sold=1&LH_Complete=1&_sop=13"
                
                logger.info(f"Scraping eBay sold items: {url}")
                rate_limiter.wait()
                
                response = await client.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Parser les produits
                product_items = soup.find_all('li', {'class': 's-item'})[:limit]
                
                for item in product_items:
                    try:
                        # Nom du produit
                        title_elem = item.find('div', {'class': 's-item__title'})
                        title = title_elem.text.strip() if title_elem else "Unknown"
                        
                        if title == "Shop on eBay":
                            continue
                        
                        # Prix
                        price_elem = item.find('span', {'class': 's-item__price'})
                        price = 0.0
                        if price_elem:
                            price_text = price_elem.text.replace('$', '').replace(',', '').strip()
                            try:
                                price = float(price_text)
                            except:
                                price = 0.0
                        
                        # URL
                        link_elem = item.find('a', {'class': 's-item__link'})
                        product_url = link_elem['href'] if link_elem and 'href' in link_elem.attrs else ""
                        
                        # Image
                        img_elem = item.find('img')
                        image_url = img_elem['src'] if img_elem and 'src' in img_elem.attrs else ""
                        
                        # Date de vente
                        sold_date_elem = item.find('span', {'class': 's-item__endedDate'})
                        sold_date = sold_date_elem.text.strip() if sold_date_elem else ""
                        
                        product = {
                            "nom": title,
                            "prix": price,
                            "url": product_url,
                            "source": "ebay",
                            "categorie": keyword,
                            "image_url": image_url,
                            "rating": 0.0,
                            "reviews_count": 0,
                            "stock_status": "sold",
                            "description": f"Sold on {sold_date}"
                        }
                        
                        products.append(product)
                        logger.info(f"Scraped eBay sold item: {title[:50]}...")
                    
                    except Exception as e:
                        logger.error(f"Error parsing eBay item: {str(e)}")
                        continue
                
                # Mettre en cache
                scraper_cache.set(cache_key, products)
                
                logger.info(f"Successfully scraped {len(products)} eBay sold items")
                return products
        
        except Exception as e:
            error = handle_scraping_error(e, "ebay", url)
            return []


# Instance globale
ebay_scraper = EbayScraper()
