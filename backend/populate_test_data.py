"""
Script to populate database with test data
"""
import sys
import os
sys.path.append('/app')

from sqlalchemy.orm import Session
from models import SessionLocal, Product, PriceHistory, Trend
from datetime import datetime, timedelta
import random

def create_test_data():
    db = SessionLocal()
    
    try:
        print("🚀 Creating test products...")
        
        # Sample products
        products_data = [
            {"nom": "Wireless Earbuds Pro", "categorie": "Electronics", "source": "Amazon"},
            {"nom": "Smart Watch Ultra", "categorie": "Electronics", "source": "AliExpress"},
            {"nom": "Portable Blender", "categorie": "Home & Kitchen", "source": "eBay"},
            {"nom": "LED Strip Lights", "categorie": "Home & Garden", "source": "Shopify"},
            {"nom": "Phone Stand Holder", "categorie": "Accessories", "source": "Amazon"},
            {"nom": "Yoga Mat Premium", "categorie": "Sports", "source": "AliExpress"},
            {"nom": "Coffee Maker Mini", "categorie": "Home & Kitchen", "source": "Amazon"},
            {"nom": "Gaming Mouse RGB", "categorie": "Electronics", "source": "eBay"},
            {"nom": "Laptop Stand Adjustable", "categorie": "Office", "source": "Shopify"},
            {"nom": "Water Bottle Smart", "categorie": "Sports", "source": "Amazon"},
            {"nom": "Desk Organizer Set", "categorie": "Office", "source": "AliExpress"},
            {"nom": "Phone Case Magnetic", "categorie": "Accessories", "source": "eBay"},
            {"nom": "Bluetooth Speaker", "categorie": "Electronics", "source": "Amazon"},
            {"nom": "Fitness Tracker Band", "categorie": "Sports", "source": "Shopify"},
            {"nom": "Car Phone Mount", "categorie": "Automotive", "source": "AliExpress"},
        ]
        
        created_products = []
        
        for i, prod_data in enumerate(products_data):
            # Random prices
            prix = round(random.uniform(15, 150), 2)
            
            product = Product(
                nom=prod_data["nom"],
                description=f"High quality {prod_data['nom'].lower()} with premium features",
                prix=prix,
                url=f"https://example.com/product/{i+1}",
                image_url=f"https://via.placeholder.com/300x300?text={prod_data['nom'].replace(' ', '+')}",
                source=prod_data["source"],
                categorie=prod_data["categorie"],
                rating=round(random.uniform(3.5, 5.0), 1),
                reviews_count=random.randint(50, 5000),
                stock_status="In Stock" if random.random() > 0.2 else "Low Stock",
                asin=f"B0{random.randint(10000, 99999)}XYZ"
            )
            
            db.add(product)
            db.flush()
            
            # Add price history
            for days_ago in range(30, 0, -5):
                price_variation = random.uniform(0.9, 1.1)
                price_history = PriceHistory(
                    product_id=product.id,
                    prix=round(prix * price_variation, 2),
                    source=prod_data["source"],
                    date=datetime.now() - timedelta(days=days_ago)
                )
                db.add(price_history)
            
            # Add trend data
            trend = Trend(
                product_id=product.id,
                score_tendance=round(random.uniform(60, 95), 1),
                volume_ventes_estime=random.randint(100, 5000),
                saturation_marche=round(random.uniform(20, 80), 2),
                marge_beneficiaire=round(prix * random.uniform(0.2, 0.5), 2),
                date_calcul=datetime.now()
            )
            db.add(trend)
            
            created_products.append(product)
            print(f"✅ Created: {product.nom} (${prix})")
        
        db.commit()
        
        print(f"\n🎉 Successfully created {len(created_products)} test products!")
        print(f"📊 Dashboard should now display data!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()

