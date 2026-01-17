import random
import time
from typing import List, Dict, Optional
import os
from loguru import logger

# Liste de User-Agents pour rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]


class ProxyRotator:
    """Gestion de la rotation des proxies"""
    
    def __init__(self):
        proxy_list = os.getenv("PROXY_LIST", "")
        self.proxies = [p.strip() for p in proxy_list.split(",") if p.strip()]
        self.current_index = 0
    
    def get_next_proxy(self) -> Optional[str]:
        """Récupérer le prochain proxy dans la liste"""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
    
    def get_random_proxy(self) -> Optional[str]:
        """Récupérer un proxy aléatoire"""
        if not self.proxies:
            return None
        return random.choice(self.proxies)


class RateLimiter:
    """Rate limiting pour éviter les bans"""
    
    def __init__(self, requests_per_minute: int = 10):
        self.requests_per_minute = requests_per_minute
        self.min_delay = 60.0 / requests_per_minute
        self.last_request_time = 0
    
    def wait(self):
        """Attendre si nécessaire pour respecter le rate limit"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay:
            sleep_time = self.min_delay - time_since_last
            logger.info(f"Rate limiting: waiting {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()


def get_random_user_agent() -> str:
    """Récupérer un User-Agent aléatoire"""
    return random.choice(USER_AGENTS)


def get_headers() -> Dict[str, str]:
    """Générer des headers HTTP aléatoires"""
    return {
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }


class ScraperCache:
    """Cache simple pour éviter de scraper les mêmes données trop souvent"""
    
    def __init__(self, cache_duration_hours: int = 6):
        self.cache = {}
        self.cache_duration = cache_duration_hours * 3600
    
    def get(self, key: str) -> Optional[Dict]:
        """Récupérer une valeur du cache"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_duration:
                logger.info(f"Cache hit for {key}")
                return data
            else:
                logger.info(f"Cache expired for {key}")
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Dict):
        """Stocker une valeur dans le cache"""
        self.cache[key] = (value, time.time())
        logger.info(f"Cached {key}")
    
    def clear(self):
        """Vider le cache"""
        self.cache.clear()
        logger.info("Cache cleared")


def handle_scraping_error(error: Exception, source: str, url: str):
    """Gestion centralisée des erreurs de scraping"""
    logger.error(f"Scraping error for {source} at {url}: {str(error)}")
    
    # Log détaillé pour debugging
    logger.exception(error)
    
    return {
        "error": True,
        "source": source,
        "url": url,
        "message": str(error),
        "timestamp": time.time()
    }


# Instances globales
proxy_rotator = ProxyRotator()
rate_limiter = RateLimiter(requests_per_minute=10)
scraper_cache = ScraperCache(cache_duration_hours=6)
