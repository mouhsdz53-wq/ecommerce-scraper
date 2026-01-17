import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from loguru import logger
from scrapers.utils import get_headers, rate_limiter, scraper_cache, handle_scraping_error
import json


class AliExpressScraper:
    """Scraper pour AliExpress - Produits tendances"""
    
    def __init__(self):
        self.base_url = "https://www.aliexpress.com"
        self.headers = get_headers()
    
    async def scrape_trending_products(self, category: str = "electronics", limit: int = 50) -> List[Dict]:
        """
        Scraper les produits tendances AliExpress
        """
        cache_key = f"aliexpress_trending_{category}"
        cached_data = scraper_cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        products = []
        
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=30.0) as client:
                # URL de recherche pour produits tendances
                url = f"{self.base_url}/wholesale?SearchText={category}&SortType=total_tranpro_desc"
                
                logger.info(f"Scraping AliExpress trending: {url}")
                rate_limiter.wait()
                
                response = await client.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Chercher les données JSON embarquées (AliExpress utilise du JavaScript)
                script_tags = soup.find_all('script')
                
                for script in script_tags:
                    if script.string and 'window.runParams' in script.string:
                        # Extraire les données JSON
                        try:
                            json_start = script.string.find('{')
                            json_end = script.string.rfind('}') + 1
                            json_data = json.loads(script.string[json_start:json_end])
                            
                            # Parser les produits depuis les données JSON
                            if 'mods' in json_data and 'itemList' in json_data['mods']:
                                items = json_data['mods']['itemList']['content'][:limit]
                                
                                for item in items:
                                    try:
                                        product = {
                                            "nom": item.get('title', {}).get('displayTitle', 'Unknown'),
                                            "prix": float(item.get('prices', {}).get('salePrice', {}).get('minPrice', 0)),
                                            "url": f"https:{item.get('productDetailUrl', '')}",
                                            "source": "aliexpress",
                                            "categorie": category,
                                            "image_url": f"https:{item.get('image', {}).get('imgUrl', '')}",
                                            "rating": float(item.get('evaluation', {}).get('starRating', 0)),
                                            "reviews_count": int(item.get('trade', {}).get('tradeDesc', '0').replace('+', '').replace('sold', '').strip() or 0),
                                            "stock_status": "in_stock"
                                        }
                                        
                                        products.append(product)
                                        logger.info(f"Scraped AliExpress product: {product['nom'][:50]}...")
                                    
                                    except Exception as e:
                                        logger.error(f"Error parsing AliExpress item: {str(e)}")
                                        continue
                            
                            break
                        
                        except json.JSONDecodeError:
                            continue
                
                # Si pas de données JSON, fallback sur parsing HTML classique
                if not products:
                    product_items = soup.find_all('div', {'class': 'list-item'})[:limit]
                    
                    for item in product_items:
                        try:
                            title_elem = item.find('a', {'class': 'item-title'})
                            title = title_elem.text.strip() if title_elem else "Unknown"
                            
                            price_elem = item.find('span', {'class': 'price-current'})
                            price = 0.0
                            if price_elem:
                                price_text = price_elem.text.replace('$', '').replace(',', '').strip()
                                try:
                                    price = float(price_text)
                                except:
                                    price = 0.0
                            
                            link_elem = item.find('a', {'class': 'item-title'})
                            product_url = link_elem['href'] if link_elem and 'href' in link_elem.attrs else ""
                            if product_url and not product_url.startswith('http'):
                                product_url = f"https:{product_url}"
                            
                            img_elem = item.find('img')
                            image_url = img_elem['src'] if img_elem and 'src' in img_elem.attrs else ""
                            if image_url and not image_url.startswith('http'):
                                image_url = f"https:{image_url}"
                            
                            product = {
                                "nom": title,
                                "prix": price,
                                "url": product_url,
                                "source": "aliexpress",
                                "categorie": category,
                                "image_url": image_url,
                                "rating": 0.0,
                                "reviews_count": 0,
                                "stock_status": "in_stock"
                            }
                            
                            products.append(product)
                            logger.info(f"Scraped AliExpress product (HTML): {title[:50]}...")
                        
                        except Exception as e:
                            logger.error(f"Error parsing AliExpress product: {str(e)}")
                            continue
                
                # Mettre en cache
                scraper_cache.set(cache_key, products)
                
                logger.info(f"Successfully scraped {len(products)} AliExpress products")
                return products
        
        except Exception as e:
            error = handle_scraping_error(e, "aliexpress", url)
            return []
    
    async def scrape_product_details(self, product_id: str) -> Optional[Dict]:
        """
        Scraper les détails d'un produit AliExpress
        """
        cache_key = f"aliexpress_product_{product_id}"
        cached_data = scraper_cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=30.0) as client:
                url = f"{self.base_url}/item/{product_id}.html"
                
                logger.info(f"Scraping AliExpress product details: {url}")
                rate_limiter.wait()
                
                response = await client.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extraire description
                description_elem = soup.find('div', {'class': 'product-description'})
                description = description_elem.text.strip() if description_elem else ""
                
                product_details = {
                    "product_id": product_id,
                    "description": description,
                    "url": url
                }
                
                scraper_cache.set(cache_key, product_details)
                
                return product_details
        
        except Exception as e:
            handle_scraping_error(e, "aliexpress", f"{self.base_url}/item/{product_id}.html")
            return None


# Instance globale
aliexpress_scraper = AliExpressScraper()
