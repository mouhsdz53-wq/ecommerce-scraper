import httpx
from typing import List, Dict, Optional
from loguru import logger
from scrapers.utils import get_headers, rate_limiter, scraper_cache, handle_scraping_error
import json


class ShopifyScraper:
    """Scraper pour Shopify stores"""
    
    def __init__(self):
        self.headers = get_headers()
    
    async def scrape_store_products(self, store_url: str, limit: int = 50) -> List[Dict]:
        """
        Scraper les produits d'un store Shopify via /products.json
        """
        cache_key = f"shopify_{store_url}"
        cached_data = scraper_cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        products = []
        
        try:
            # Nettoyer l'URL
            if not store_url.startswith('http'):
                store_url = f"https://{store_url}"
            
            if not store_url.endswith('/'):
                store_url += '/'
            
            async with httpx.AsyncClient(headers=self.headers, timeout=30.0) as client:
                url = f"{store_url}products.json?limit={limit}"
                
                logger.info(f"Scraping Shopify store: {url}")
                rate_limiter.wait()
                
                response = await client.get(url)
                response.raise_for_status()
                
                data = response.json()
                
                if 'products' in data:
                    for item in data['products']:
                        try:
                            # Récupérer le premier variant pour le prix
                            variant = item.get('variants', [{}])[0]
                            
                            product = {
                                "nom": item.get('title', 'Unknown'),
                                "prix": float(variant.get('price', 0)),
                                "url": f"{store_url}products/{item.get('handle', '')}",
                                "source": "shopify",
                                "categorie": item.get('product_type', 'general'),
                                "image_url": item.get('images', [{}])[0].get('src', '') if item.get('images') else '',
                                "rating": 0.0,
                                "reviews_count": 0,
                                "stock_status": "in_stock" if variant.get('available', False) else "out_of_stock",
                                "description": item.get('body_html', '')[:500]  # Limiter la description
                            }
                            
                            products.append(product)
                            logger.info(f"Scraped Shopify product: {product['nom'][:50]}...")
                        
                        except Exception as e:
                            logger.error(f"Error parsing Shopify product: {str(e)}")
                            continue
                
                # Mettre en cache
                scraper_cache.set(cache_key, products)
                
                logger.info(f"Successfully scraped {len(products)} Shopify products from {store_url}")
                return products
        
        except Exception as e:
            error = handle_scraping_error(e, "shopify", store_url)
            return []
    
    async def detect_trending_stores(self, niche: str = "fashion") -> List[str]:
        """
        Détecter les stores Shopify en croissance (liste statique pour démo)
        En production, utiliser des APIs comme BuiltWith ou similaire
        """
        # Liste de stores Shopify populaires par niche
        trending_stores = {
            "fashion": [
                "gymshark.com",
                "fashionnova.com",
                "mvmt.com"
            ],
            "electronics": [
                "anker.com",
                "wyze.com"
            ],
            "home": [
                "allbirds.com",
                "casper.com"
            ]
        }
        
        return trending_stores.get(niche, [])


# Instance globale
shopify_scraper = ShopifyScraper()
