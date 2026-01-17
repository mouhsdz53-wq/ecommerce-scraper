from celery_app import app
from sqlalchemy.orm import Session
from models import SessionLocal, Product, PriceHistory, Trend
from scrapers.amazon_scraper import amazon_scraper
from scrapers.aliexpress_scraper import aliexpress_scraper
from scrapers.ebay_scraper import ebay_scraper
from scrapers.shopify_scraper import shopify_scraper
from loguru import logger
from datetime import datetime
from decimal import Decimal
import asyncio


@app.task(name='tasks.scraping_tasks.scrape_all_sources')
def scrape_all_sources():
    """
    Tâche de scraping quotidien pour toutes les sources
    """
    logger.info("Starting daily scraping task for all sources")
    
    db = SessionLocal()
    
    try:
        # Catégories à scraper
        categories = ["electronics", "fashion", "home", "sports"]
        
        total_scraped = 0
        
        for category in categories:
            logger.info(f"Scraping category: {category}")
            
            # Amazon
            try:
                amazon_products = asyncio.run(amazon_scraper.scrape_bestsellers(category=category, limit=25))
                total_scraped += save_products_to_db(db, amazon_products)
            except Exception as e:
                logger.error(f"Error scraping Amazon {category}: {str(e)}")
            
            # AliExpress
            try:
                aliexpress_products = asyncio.run(aliexpress_scraper.scrape_trending_products(category=category, limit=25))
                total_scraped += save_products_to_db(db, aliexpress_products)
            except Exception as e:
                logger.error(f"Error scraping AliExpress {category}: {str(e)}")
            
            # eBay
            try:
                ebay_products = asyncio.run(ebay_scraper.scrape_sold_items(keyword=category, limit=25))
                total_scraped += save_products_to_db(db, ebay_products)
            except Exception as e:
                logger.error(f"Error scraping eBay {category}: {str(e)}")
        
        # Shopify stores
        try:
            stores = asyncio.run(shopify_scraper.detect_trending_stores(niche="fashion"))
            for store in stores[:3]:  # Limiter à 3 stores
                shopify_products = asyncio.run(shopify_scraper.scrape_store_products(store, limit=20))
                total_scraped += save_products_to_db(db, shopify_products)
        except Exception as e:
            logger.error(f"Error scraping Shopify stores: {str(e)}")
        
        logger.info(f"Daily scraping completed. Total products scraped: {total_scraped}")
        return {"status": "success", "total_scraped": total_scraped}
    
    except Exception as e:
        logger.error(f"Error in scrape_all_sources: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


@app.task(name='tasks.scraping_tasks.update_prices')
def update_prices():
    """
    Mise à jour des prix toutes les 6h pour les produits suivis
    """
    logger.info("Starting price update task")
    
    db = SessionLocal()
    
    try:
        # Récupérer tous les produits actifs
        products = db.query(Product).limit(100).all()  # Limiter pour ne pas surcharger
        
        updated_count = 0
        
        for product in products:
            try:
                # Enregistrer le prix actuel dans l'historique
                price_history = PriceHistory(
                    product_id=product.id,
                    prix=product.prix,
                    source=product.source,
                    date=datetime.utcnow()
                )
                
                db.add(price_history)
                updated_count += 1
            
            except Exception as e:
                logger.error(f"Error updating price for product {product.id}: {str(e)}")
                continue
        
        db.commit()
        
        logger.info(f"Price update completed. {updated_count} prices updated")
        return {"status": "success", "updated_count": updated_count}
    
    except Exception as e:
        logger.error(f"Error in update_prices: {str(e)}")
        db.rollback()
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


@app.task(name='tasks.scraping_tasks.calculate_trends')
def calculate_trends():
    """
    Calcul quotidien des scores de tendance
    """
    logger.info("Starting trend calculation task")
    
    db = SessionLocal()
    
    try:
        products = db.query(Product).all()
        
        calculated_count = 0
        
        for product in products:
            try:
                # Calcul simple du score de tendance basé sur reviews et rating
                score_tendance = 0.0
                
                if product.reviews_count and product.rating:
                    # Score basé sur nombre de reviews et rating
                    score_tendance = min(100, (product.reviews_count / 100) * float(product.rating) * 10)
                
                # Estimer le volume de ventes (basé sur reviews)
                volume_ventes_estime = product.reviews_count * 10 if product.reviews_count else 0
                
                # Calculer la saturation (nombre de concurrents)
                competitors_count = db.query(Product).filter(
                    Product.nom.ilike(f"%{product.nom[:20]}%"),
                    Product.id != product.id
                ).count()
                
                saturation_marche = min(100, competitors_count * 5)
                
                # Créer ou mettre à jour le trend
                trend = Trend(
                    product_id=product.id,
                    score_tendance=Decimal(str(score_tendance)),
                    volume_ventes_estime=volume_ventes_estime,
                    saturation_marche=Decimal(str(saturation_marche)),
                    date_calcul=datetime.utcnow()
                )
                
                db.add(trend)
                calculated_count += 1
            
            except Exception as e:
                logger.error(f"Error calculating trend for product {product.id}: {str(e)}")
                continue
        
        db.commit()
        
        logger.info(f"Trend calculation completed. {calculated_count} trends calculated")
        return {"status": "success", "calculated_count": calculated_count}
    
    except Exception as e:
        logger.error(f"Error in calculate_trends: {str(e)}")
        db.rollback()
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


def save_products_to_db(db: Session, products: list) -> int:
    """
    Sauvegarder les produits dans la base de données
    """
    saved_count = 0
    
    for product_data in products:
        try:
            # Vérifier si le produit existe déjà
            existing = db.query(Product).filter(
                Product.url == product_data.get('url')
            ).first()
            
            if existing:
                # Mettre à jour le prix
                existing.prix = product_data.get('prix', 0)
                existing.date_scrape = datetime.utcnow()
            else:
                # Créer nouveau produit
                product = Product(
                    nom=product_data.get('nom', 'Unknown'),
                    categorie=product_data.get('categorie'),
                    prix=product_data.get('prix', 0),
                    url=product_data.get('url', ''),
                    source=product_data.get('source', 'unknown'),
                    image_url=product_data.get('image_url'),
                    description=product_data.get('description'),
                    asin=product_data.get('asin'),
                    reviews_count=product_data.get('reviews_count', 0),
                    rating=product_data.get('rating'),
                    stock_status=product_data.get('stock_status', 'unknown'),
                    date_scrape=datetime.utcnow()
                )
                
                db.add(product)
            
            saved_count += 1
        
        except Exception as e:
            logger.error(f"Error saving product: {str(e)}")
            continue
    
    db.commit()
    return saved_count
