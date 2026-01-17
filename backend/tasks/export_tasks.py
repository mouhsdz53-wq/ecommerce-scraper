from celery_app import app
from sqlalchemy.orm import Session
from models import SessionLocal, Product, Trend
from loguru import logger
import pandas as pd
from datetime import datetime
import os


@app.task(name='tasks.export_tasks.export_weekly_report')
def export_weekly_report():
    """
    Export hebdomadaire des données en CSV/Excel
    """
    logger.info("Starting weekly export task")
    
    db = SessionLocal()
    
    try:
        # Récupérer les top produits tendances
        top_products = db.query(Product, Trend).join(Trend).order_by(
            Trend.score_tendance.desc()
        ).limit(100).all()
        
        # Préparer les données pour export
        data = []
        for product, trend in top_products:
            data.append({
                "ID": product.id,
                "Nom": product.nom,
                "Catégorie": product.categorie,
                "Prix": float(product.prix),
                "Source": product.source,
                "Score Tendance": float(trend.score_tendance),
                "Volume Ventes Estimé": trend.volume_ventes_estime,
                "Saturation Marché": float(trend.saturation_marche) if trend.saturation_marche else 0,
                "Marge Bénéficiaire": float(trend.marge_beneficiaire) if trend.marge_beneficiaire else 0,
                "Rating": float(product.rating) if product.rating else 0,
                "Reviews": product.reviews_count,
                "URL": product.url
            })
        
        # Créer DataFrame
        df = pd.DataFrame(data)
        
        # Créer dossier exports si n'existe pas
        exports_dir = "exports"
        os.makedirs(exports_dir, exist_ok=True)
        
        # Générer nom de fichier avec date
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"{exports_dir}/weekly_report_{timestamp}.csv"
        excel_filename = f"{exports_dir}/weekly_report_{timestamp}.xlsx"
        
        # Exporter en CSV
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        logger.info(f"CSV export saved: {csv_filename}")
        
        # Exporter en Excel
        df.to_excel(excel_filename, index=False, engine='openpyxl')
        logger.info(f"Excel export saved: {excel_filename}")
        
        return {
            "status": "success",
            "csv_file": csv_filename,
            "excel_file": excel_filename,
            "products_count": len(data)
        }
    
    except Exception as e:
        logger.error(f"Error in export_weekly_report: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


@app.task(name='tasks.export_tasks.export_custom')
def export_custom(filters: dict = None):
    """
    Export personnalisé avec filtres
    """
    logger.info(f"Starting custom export with filters: {filters}")
    
    db = SessionLocal()
    
    try:
        query = db.query(Product)
        
        # Appliquer les filtres
        if filters:
            if 'categorie' in filters:
                query = query.filter(Product.categorie == filters['categorie'])
            if 'source' in filters:
                query = query.filter(Product.source == filters['source'])
            if 'prix_min' in filters:
                query = query.filter(Product.prix >= filters['prix_min'])
            if 'prix_max' in filters:
                query = query.filter(Product.prix <= filters['prix_max'])
        
        products = query.all()
        
        # Préparer les données
        data = []
        for product in products:
            data.append({
                "ID": product.id,
                "Nom": product.nom,
                "Catégorie": product.categorie,
                "Prix": float(product.prix),
                "Source": product.source,
                "Rating": float(product.rating) if product.rating else 0,
                "Reviews": product.reviews_count,
                "URL": product.url,
                "Date Scrape": product.date_scrape.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        df = pd.DataFrame(data)
        
        # Export
        exports_dir = "exports"
        os.makedirs(exports_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{exports_dir}/custom_export_{timestamp}.csv"
        
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"Custom export saved: {filename}")
        
        return {
            "status": "success",
            "file": filename,
            "products_count": len(data)
        }
    
    except Exception as e:
        logger.error(f"Error in export_custom: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()
