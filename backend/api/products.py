from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from datetime import datetime, timedelta
from models import get_db, Product, PriceHistory, Competitor, Trend
from pydantic import BaseModel
from decimal import Decimal

router = APIRouter()


# Pydantic schemas
class ProductResponse(BaseModel):
    id: int
    nom: str
    categorie: Optional[str]
    prix: Decimal
    url: str
    source: str
    image_url: Optional[str]
    rating: Optional[Decimal]
    reviews_count: int
    date_scrape: datetime
    
    class Config:
        from_attributes = True


class ProductDetailResponse(ProductResponse):
    description: Optional[str]
    asin: Optional[str]
    stock_status: Optional[str]
    
    class Config:
        from_attributes = True


class PriceHistoryResponse(BaseModel):
    id: int
    prix: Decimal
    date: datetime
    source: str
    
    class Config:
        from_attributes = True


class CompetitorResponse(BaseModel):
    id: int
    vendeur: str
    prix: Decimal
    url: Optional[str]
    stock: Optional[int]
    rating: Optional[Decimal]
    date_scrape: datetime
    
    class Config:
        from_attributes = True


class TrendResponse(BaseModel):
    score_tendance: Decimal
    volume_ventes_estime: Optional[int]
    saturation_marche: Optional[Decimal]
    marge_beneficiaire: Optional[Decimal]
    date_calcul: datetime
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    categorie: Optional[str] = None,
    source: Optional[str] = None,
    prix_min: Optional[float] = None,
    prix_max: Optional[float] = None,
    sort_by: str = "date_scrape",
    db: Session = Depends(get_db)
):
    """
    Récupérer la liste des produits avec filtres avancés
    """
    query = db.query(Product)
    
    # Filtres
    if categorie:
        query = query.filter(Product.categorie == categorie)
    if source:
        query = query.filter(Product.source == source)
    if prix_min:
        query = query.filter(Product.prix >= prix_min)
    if prix_max:
        query = query.filter(Product.prix <= prix_max)
    
    # Tri
    if sort_by == "prix_asc":
        query = query.order_by(Product.prix.asc())
    elif sort_by == "prix_desc":
        query = query.order_by(Product.prix.desc())
    elif sort_by == "rating":
        query = query.order_by(desc(Product.rating))
    else:
        query = query.order_by(desc(Product.date_scrape))
    
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/trending", response_model=List[ProductResponse])
async def get_trending_products(
    limit: int = 100,
    categorie: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Récupérer le top 100 des produits tendances
    """
    query = db.query(Product).join(Trend)
    
    if categorie:
        query = query.filter(Product.categorie == categorie)
    
    products = query.order_by(desc(Trend.score_tendance)).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductDetailResponse)
async def get_product_detail(product_id: int, db: Session = Depends(get_db)):
    """
    Récupérer les détails d'un produit
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/{product_id}/history", response_model=List[PriceHistoryResponse])
async def get_price_history(
    product_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Récupérer l'historique des prix d'un produit
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    history = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id,
        PriceHistory.date >= start_date
    ).order_by(PriceHistory.date.asc()).all()
    
    return history


@router.get("/{product_id}/competitors", response_model=List[CompetitorResponse])
async def get_competitors(product_id: int, db: Session = Depends(get_db)):
    """
    Récupérer la liste des concurrents pour un produit
    """
    competitors = db.query(Competitor).filter(
        Competitor.product_id == product_id
    ).order_by(Competitor.prix.asc()).all()
    
    return competitors


@router.get("/{product_id}/trend", response_model=TrendResponse)
async def get_product_trend(product_id: int, db: Session = Depends(get_db)):
    """
    Récupérer les données de tendance d'un produit
    """
    trend = db.query(Trend).filter(
        Trend.product_id == product_id
    ).order_by(desc(Trend.date_calcul)).first()
    
    if not trend:
        raise HTTPException(status_code=404, detail="Trend data not found")
    
    return trend


@router.post("/compare")
async def compare_products(product_ids: List[int], db: Session = Depends(get_db)):
    """
    Comparer plusieurs produits
    """
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    
    if len(products) != len(product_ids):
        raise HTTPException(status_code=404, detail="Some products not found")
    
    comparison = []
    for product in products:
        trend = db.query(Trend).filter(
            Trend.product_id == product.id
        ).order_by(desc(Trend.date_calcul)).first()
        
        comparison.append({
            "product": ProductDetailResponse.from_orm(product),
            "trend": TrendResponse.from_orm(trend) if trend else None
        })
    
    return comparison


@router.get("/categories/list")
async def get_categories(db: Session = Depends(get_db)):
    """
    Récupérer la liste des catégories disponibles
    """
    categories = db.query(Product.categorie).distinct().all()
    return [cat[0] for cat in categories if cat[0]]


@router.get("/sources/list")
async def get_sources(db: Session = Depends(get_db)):
    """
    Récupérer la liste des sources disponibles
    """
    sources = db.query(Product.source).distinct().all()
    return [src[0] for src in sources if src[0]]
