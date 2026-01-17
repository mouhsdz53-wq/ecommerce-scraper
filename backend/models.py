from sqlalchemy import create_engine, Column, Integer, String, Numeric, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://scraper_user:scraper_password@localhost:5432/ecommerce_scraper")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(500), nullable=False)
    categorie = Column(String(200))
    prix = Column(Numeric(10, 2), nullable=False)
    url = Column(Text, nullable=False)
    source = Column(String(50), nullable=False)
    date_scrape = Column(DateTime, default=datetime.utcnow)
    image_url = Column(Text)
    description = Column(Text)
    asin = Column(String(20))
    reviews_count = Column(Integer, default=0)
    rating = Column(Numeric(3, 2))
    stock_status = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")
    competitors = relationship("Competitor", back_populates="product", cascade="all, delete-orphan")
    trends = relationship("Trend", back_populates="product", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="product", cascade="all, delete-orphan")
    sentiment = relationship("SentimentAnalysis", back_populates="product", cascade="all, delete-orphan")


class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    prix = Column(Numeric(10, 2), nullable=False)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    source = Column(String(50), nullable=False)
    
    product = relationship("Product", back_populates="price_history")


class Competitor(Base):
    __tablename__ = "competitors"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    vendeur = Column(String(200), nullable=False)
    prix = Column(Numeric(10, 2), nullable=False)
    url = Column(Text)
    stock = Column(Integer)
    rating = Column(Numeric(3, 2))
    date_scrape = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="competitors")


class Trend(Base):
    __tablename__ = "trends"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    score_tendance = Column(Numeric(5, 2), nullable=False)
    volume_ventes_estime = Column(Integer)
    saturation_marche = Column(Numeric(5, 2))
    marge_beneficiaire = Column(Numeric(10, 2))
    date_calcul = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="trends")


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    type_alerte = Column(String(100), nullable=False)
    seuil = Column(Numeric(10, 2))
    actif = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="alerts")


class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    sentiment_score = Column(Numeric(3, 2))
    positive_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    date_analyse = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="sentiment")


class ShopifyStore(Base):
    __tablename__ = "shopify_stores"
    
    id = Column(Integer, primary_key=True, index=True)
    store_url = Column(Text, nullable=False, unique=True)
    store_name = Column(String(200))
    products_count = Column(Integer, default=0)
    growth_rate = Column(Numeric(5, 2))
    last_scrape = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
