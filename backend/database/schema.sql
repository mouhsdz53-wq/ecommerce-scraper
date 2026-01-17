-- E-Commerce Scraper Database Schema

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(500) NOT NULL,
    categorie VARCHAR(200),
    prix DECIMAL(10, 2) NOT NULL,
    url TEXT NOT NULL,
    source VARCHAR(50) NOT NULL, -- amazon, aliexpress, ebay, shopify
    date_scrape TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image_url TEXT,
    description TEXT,
    asin VARCHAR(20), -- Amazon ASIN
    reviews_count INTEGER DEFAULT 0,
    rating DECIMAL(3, 2),
    stock_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Price history table
CREATE TABLE IF NOT EXISTS price_history (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    prix DECIMAL(10, 2) NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(50) NOT NULL
);

-- Competitors table
CREATE TABLE IF NOT EXISTS competitors (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    vendeur VARCHAR(200) NOT NULL,
    prix DECIMAL(10, 2) NOT NULL,
    url TEXT,
    stock INTEGER,
    rating DECIMAL(3, 2),
    date_scrape TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trends table
CREATE TABLE IF NOT EXISTS trends (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    score_tendance DECIMAL(5, 2) NOT NULL, -- 0-100
    volume_ventes_estime INTEGER,
    saturation_marche DECIMAL(5, 2), -- 0-100
    marge_beneficiaire DECIMAL(10, 2),
    date_calcul TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alerts table
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER, -- Pour multi-utilisateurs futur
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    type_alerte VARCHAR(100) NOT NULL, -- price_drop, new_viral, low_saturation
    seuil DECIMAL(10, 2), -- Seuil de déclenchement
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sentiment analysis table
CREATE TABLE IF NOT EXISTS sentiment_analysis (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    sentiment_score DECIMAL(3, 2), -- -1 to 1
    positive_count INTEGER DEFAULT 0,
    negative_count INTEGER DEFAULT 0,
    neutral_count INTEGER DEFAULT 0,
    date_analyse TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Shopify stores tracker
CREATE TABLE IF NOT EXISTS shopify_stores (
    id SERIAL PRIMARY KEY,
    store_url TEXT NOT NULL UNIQUE,
    store_name VARCHAR(200),
    products_count INTEGER DEFAULT 0,
    growth_rate DECIMAL(5, 2),
    last_scrape TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_products_categorie ON products(categorie);
CREATE INDEX IF NOT EXISTS idx_products_source ON products(source);
CREATE INDEX IF NOT EXISTS idx_products_date_scrape ON products(date_scrape);
CREATE INDEX IF NOT EXISTS idx_price_history_product_id ON price_history(product_id);
CREATE INDEX IF NOT EXISTS idx_price_history_date ON price_history(date);
CREATE INDEX IF NOT EXISTS idx_competitors_product_id ON competitors(product_id);
CREATE INDEX IF NOT EXISTS idx_trends_product_id ON trends(product_id);
CREATE INDEX IF NOT EXISTS idx_trends_score_tendance ON trends(score_tendance DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_product_id ON alerts(product_id);
CREATE INDEX IF NOT EXISTS idx_alerts_actif ON alerts(actif);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_products_updated_at
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
