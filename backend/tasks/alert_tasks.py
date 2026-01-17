from celery_app import app
from sqlalchemy.orm import Session
from models import SessionLocal, Alert, Product, PriceHistory
from loguru import logger
from datetime import datetime, timedelta
from decimal import Decimal
import os
import httpx


@app.task(name='tasks.alert_tasks.check_alerts')
def check_alerts():
    """
    Vérifier les alertes toutes les heures et envoyer des notifications
    """
    logger.info("Starting alert check task")
    
    db = SessionLocal()
    
    try:
        # Récupérer toutes les alertes actives
        alerts = db.query(Alert).filter(Alert.actif == True).all()
        
        triggered_alerts = []
        
        for alert in alerts:
            try:
                product = db.query(Product).filter(Product.id == alert.product_id).first()
                
                if not product:
                    continue
                
                should_trigger = False
                message = ""
                
                # Vérifier selon le type d'alerte
                if alert.type_alerte == "price_drop":
                    # Vérifier si le prix a baissé sous le seuil
                    if alert.seuil and product.prix <= alert.seuil:
                        should_trigger = True
                        message = f"🔔 Prix baissé ! {product.nom[:50]} est maintenant à ${product.prix} (seuil: ${alert.seuil})"
                
                elif alert.type_alerte == "new_viral":
                    # Vérifier si le produit devient viral (augmentation rapide des reviews)
                    recent_history = db.query(PriceHistory).filter(
                        PriceHistory.product_id == product.id,
                        PriceHistory.date >= datetime.utcnow() - timedelta(days=7)
                    ).count()
                    
                    if recent_history > 10:  # Activité élevée
                        should_trigger = True
                        message = f"🔥 Produit viral détecté ! {product.nom[:50]} - {product.reviews_count} reviews"
                
                elif alert.type_alerte == "low_saturation":
                    # Vérifier si le marché est peu saturé
                    competitors_count = db.query(Product).filter(
                        Product.nom.ilike(f"%{product.nom[:20]}%"),
                        Product.id != product.id
                    ).count()
                    
                    if competitors_count < 5:  # Peu de concurrence
                        should_trigger = True
                        message = f"💎 Opportunité ! {product.nom[:50]} - Seulement {competitors_count} concurrents"
                
                if should_trigger:
                    triggered_alerts.append({
                        "alert_id": alert.id,
                        "product_id": product.id,
                        "message": message
                    })
                    
                    # Envoyer notification
                    send_telegram_notification(message)
                    send_email_notification(message)
            
            except Exception as e:
                logger.error(f"Error checking alert {alert.id}: {str(e)}")
                continue
        
        logger.info(f"Alert check completed. {len(triggered_alerts)} alerts triggered")
        return {"status": "success", "triggered_count": len(triggered_alerts), "alerts": triggered_alerts}
    
    except Exception as e:
        logger.error(f"Error in check_alerts: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


def send_telegram_notification(message: str):
    """
    Envoyer une notification Telegram
    """
    try:
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        if not bot_token or not chat_id:
            logger.warning("Telegram credentials not configured")
            return
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = httpx.post(url, json=payload, timeout=10.0)
        response.raise_for_status()
        
        logger.info(f"Telegram notification sent: {message[:50]}...")
    
    except Exception as e:
        logger.error(f"Error sending Telegram notification: {str(e)}")


def send_email_notification(message: str):
    """
    Envoyer une notification par email (SendGrid)
    """
    try:
        api_key = os.getenv("SENDGRID_API_KEY")
        from_email = os.getenv("FROM_EMAIL")
        
        if not api_key or not from_email:
            logger.warning("Email credentials not configured")
            return
        
        # TODO: Implémenter l'envoi d'email avec SendGrid
        logger.info(f"Email notification would be sent: {message[:50]}...")
    
    except Exception as e:
        logger.error(f"Error sending email notification: {str(e)}")
