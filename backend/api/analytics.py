from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta
from models import get_db, Product, PriceHistory, Competitor, Trend
from pydantic import BaseModel
from decimal import Decimal

router = APIRouter()


class ProfitAnalysis(BaseModel):
    product_id: int
    product_name: str
    aliexpress_price: Optional[Decimal]
    amazon_price: Optional[Decimal]
    marge_brute: Optional[Decimal]
    marge_nette: Optional[Decimal]  # Après shipping, taxes, ads
    roi_percentage: Optional[Decimal]


class SaturationScore(BaseModel):
    product_id: int
    product_name: str
    competitors_count: int
    saturation_score: Decimal  # 0-100
    market_opportunity: str  # low, medium, high


class TrendPrediction(BaseModel):
    product_id: int
    product_name: str
    current_trend_score: Decimal
    predicted_trend_30d: Decimal
    trend_direction: str  # rising, stable, declining


@router.get("/profit", response_model=List[ProfitAnalysis])
async def calculate_profit_potential(
    limit: int = 50,
    min_margin: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    Calculer le potentiel de profit (prix AliExpress vs Amazon)
    """
    # Récupérer les produits avec prix AliExpress et Amazon
    products = db.query(Product).all()
    
    profit_analysis = []
    
    for product in products:
        # Trouver le prix le plus bas sur AliExpress
        aliexpress_price = db.query(func.min(Product.prix)).filter(
            Product.nom.ilike(f"%{product.nom[:20]}%"),
            Product.source == "aliexpress"
        ).scalar()
        
        # Trouver le prix moyen sur Amazon
        amazon_price = db.query(func.avg(Product.prix)).filter(
            Product.nom.ilike(f"%{product.nom[:20]}%"),
            Product.source == "amazon"
        ).scalar()
        
        if aliexpress_price and amazon_price:
            marge_brute = amazon_price - aliexpress_price
            
            # Estimation des coûts (shipping 15%, taxes 10%, ads 20%)
            costs = aliexpress_price * Decimal('0.45')
            marge_nette = marge_brute - costs
            
            roi = (marge_nette / aliexpress_price) * 100 if aliexpress_price > 0 else 0
            
            if min_margin is None or marge_nette >= min_margin:
                profit_analysis.append(ProfitAnalysis(
                    product_id=product.id,
                    product_name=product.nom,
                    aliexpress_price=aliexpress_price,
                    amazon_price=amazon_price,
                    marge_brute=marge_brute,
                    marge_nette=marge_nette,
                    roi_percentage=roi
                ))
    
    # Trier par ROI décroissant
    profit_analysis.sort(key=lambda x: x.roi_percentage or 0, reverse=True)
    
    return profit_analysis[:limit]


@router.get("/saturation", response_model=List[SaturationScore])
async def analyze_market_saturation(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Analyser la saturation du marché pour chaque produit
    """
    products = db.query(Product).all()
    
    saturation_scores = []
    
    for product in products:
        # Compter le nombre de concurrents
        competitors_count = db.query(Competitor).filter(
            Competitor.product_id == product.id
        ).count()
        
        # Calculer le score de saturation (0-100)
        # Plus il y a de concurrents, plus le marché est saturé
        if competitors_count == 0:
            saturation_score = Decimal('0')
            opportunity = "high"
        elif competitors_count < 10:
            saturation_score = Decimal(competitors_count * 5)
            opportunity = "high"
        elif competitors_count < 50:
            saturation_score = Decimal(50 + (competitors_count - 10) * 1.25)
            opportunity = "medium"
        else:
            saturation_score = Decimal('100')
            opportunity = "low"
        
        saturation_scores.append(SaturationScore(
            product_id=product.id,
            product_name=product.nom,
            competitors_count=competitors_count,
            saturation_score=saturation_score,
            market_opportunity=opportunity
        ))
    
    # Trier par opportunité (saturation faible = opportunité élevée)
    saturation_scores.sort(key=lambda x: x.saturation_score)
    
    return saturation_scores[:limit]


@router.get("/trends/predictions", response_model=List[TrendPrediction])
async def predict_trends(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Prédire les tendances futures basées sur l'historique
    """
    products = db.query(Product).all()
    
    predictions = []
    
    for product in products:
        # Récupérer les tendances des 30 derniers jours
        trends = db.query(Trend).filter(
            Trend.product_id == product.id,
            Trend.date_calcul >= datetime.utcnow() - timedelta(days=30)
        ).order_by(Trend.date_calcul.asc()).all()
        
        if len(trends) >= 2:
            current_score = trends[-1].score_tendance
            
            # Calcul simple de la tendance (régression linéaire basique)
            scores = [float(t.score_tendance) for t in trends]
            avg_change = (scores[-1] - scores[0]) / len(scores)
            
            predicted_score = Decimal(scores[-1] + (avg_change * 30))
            
            if avg_change > 1:
                direction = "rising"
            elif avg_change < -1:
                direction = "declining"
            else:
                direction = "stable"
            
            predictions.append(TrendPrediction(
                product_id=product.id,
                product_name=product.nom,
                current_trend_score=current_score,
                predicted_trend_30d=predicted_score,
                trend_direction=direction
            ))
    
    # Trier par tendance prédite décroissante
    predictions.sort(key=lambda x: x.predicted_trend_30d, reverse=True)
    
    return predictions[:limit]


@router.get("/seasonal")
async def detect_seasonal_products(db: Session = Depends(get_db)):
    """
    Détecter les produits saisonniers basés sur les patterns de ventes
    """
    # Récupérer les produits avec historique de prix sur 90+ jours
    seasonal_products = []
    
    products = db.query(Product).all()
    
    for product in products:
        price_history = db.query(PriceHistory).filter(
            PriceHistory.product_id == product.id,
            PriceHistory.date >= datetime.utcnow() - timedelta(days=90)
        ).all()
        
        if len(price_history) >= 30:
            # Analyser les variations de prix par mois
            monthly_avg = {}
            for record in price_history:
                month = record.date.month
                if month not in monthly_avg:
                    monthly_avg[month] = []
                monthly_avg[month].append(float(record.prix))
            
            # Calculer la variance
            if len(monthly_avg) >= 2:
                averages = [sum(prices)/len(prices) for prices in monthly_avg.values()]
                variance = max(averages) - min(averages)
                
                # Si variance > 20% du prix moyen, considéré comme saisonnier
                avg_price = sum(averages) / len(averages)
                if variance / avg_price > 0.2:
                    seasonal_products.append({
                        "product_id": product.id,
                        "product_name": product.nom,
                        "price_variance": round(variance, 2),
                        "is_seasonal": True,
                        "peak_month": max(monthly_avg, key=lambda k: sum(monthly_avg[k])/len(monthly_avg[k]))
                    })
    
    return seasonal_products


@router.get("/dashboard/summary")
async def get_dashboard_summary(db: Session = Depends(get_db)):
    """
    Récupérer un résumé pour le dashboard principal
    """
    total_products = db.query(Product).count()
    
    # Top 5 produits tendances
    top_trending = db.query(Product, Trend).join(Trend).order_by(
        desc(Trend.score_tendance)
    ).limit(5).all()
    
    # Meilleurs opportunités de profit
    top_profit = await calculate_profit_potential(limit=5, db=db)
    
    # Marchés peu saturés
    low_saturation = await analyze_market_saturation(limit=5, db=db)
    
    return {
        "total_products": total_products,
        "top_trending": [{"id": p.id, "nom": p.nom, "score": t.score_tendance} for p, t in top_trending],
        "top_profit_opportunities": top_profit,
        "low_saturation_markets": low_saturation
    }
