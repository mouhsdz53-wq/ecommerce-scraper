'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

interface DashboardSummary {
    total_products: number
    top_trending: Array<{ id: number; nom: string; score: number }>
    top_profit_opportunities: Array<any>
    low_saturation_markets: Array<any>
}

export default function HomePage() {
    const [summary, setSummary] = useState<DashboardSummary | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchDashboardSummary()
    }, [])

    const fetchDashboardSummary = async () => {
        try {
            // Auto-detect Codespaces URL
            let apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

            // If running in Codespaces, use the forwarded port URL
            if (typeof window !== 'undefined' && window.location.hostname.includes('app.github.dev')) {
                const baseUrl = window.location.origin.replace('-3000', '-8000')
                apiUrl = baseUrl
            }

            const response = await fetch(`${apiUrl}/api/analytics/dashboard/summary`)
            const data = await response.json()
            setSummary(data)
        } catch (error) {
            console.error('Error fetching dashboard summary:', error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-pulse-slow text-6xl mb-4">🔍</div>
                    <p className="text-dark-muted">Chargement du dashboard...</p>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen p-8">
            {/* Header */}
            <header className="mb-12 animate-fade-in">
                <h1 className="text-5xl font-bold mb-2 bg-gradient-to-r from-accent-primary to-accent-success bg-clip-text text-transparent">
                    E-Commerce Scraper
                </h1>
                <p className="text-dark-muted text-lg">
                    Plateforme de veille e-commerce pour identifier les produits tendances
                </p>
            </header>

            {/* Navigation */}
            <nav className="mb-12 flex gap-4 flex-wrap">
                <Link href="/products" className="btn btn-primary">
                    📦 Produits
                </Link>
                <Link href="/trending" className="btn btn-secondary">
                    🔥 Tendances
                </Link>
                <Link href="/analytics" className="btn btn-secondary">
                    📊 Analytics
                </Link>
                <Link href="/alerts" className="btn btn-secondary">
                    🔔 Alertes
                </Link>
            </nav>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
                <div className="card animate-fade-in">
                    <div className="text-dark-muted text-sm mb-2">Total Produits</div>
                    <div className="text-4xl font-bold text-accent-primary">
                        {summary?.total_products || 0}
                    </div>
                </div>

                <div className="card animate-fade-in" style={{ animationDelay: '0.1s' }}>
                    <div className="text-dark-muted text-sm mb-2">Produits Tendances</div>
                    <div className="text-4xl font-bold text-accent-success">
                        {summary?.top_trending?.length || 0}
                    </div>
                </div>

                <div className="card animate-fade-in" style={{ animationDelay: '0.2s' }}>
                    <div className="text-dark-muted text-sm mb-2">Opportunités Profit</div>
                    <div className="text-4xl font-bold text-accent-warning">
                        {summary?.top_profit_opportunities?.length || 0}
                    </div>
                </div>

                <div className="card animate-fade-in" style={{ animationDelay: '0.3s' }}>
                    <div className="text-dark-muted text-sm mb-2">Marchés Peu Saturés</div>
                    <div className="text-4xl font-bold text-accent-danger">
                        {summary?.low_saturation_markets?.length || 0}
                    </div>
                </div>
            </div>

            {/* Top Trending Products */}
            <div className="mb-12">
                <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                    <span>🔥</span> Top Produits Tendances
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {summary?.top_trending?.map((product, index) => (
                        <div
                            key={product.id}
                            className="card animate-fade-in"
                            style={{ animationDelay: `${index * 0.1}s` }}
                        >
                            <div className="flex justify-between items-start mb-3">
                                <h3 className="font-semibold text-lg line-clamp-2">
                                    {product.nom}
                                </h3>
                                <span className="badge badge-success ml-2">
                                    {product.score.toFixed(1)}
                                </span>
                            </div>
                            <Link
                                href={`/products/${product.id}`}
                                className="text-accent-primary text-sm hover:underline"
                            >
                                Voir détails →
                            </Link>
                        </div>
                    ))}
                </div>
            </div>

            {/* Top Profit Opportunities */}
            <div className="mb-12">
                <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                    <span>💰</span> Meilleures Opportunités de Profit
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {summary?.top_profit_opportunities?.slice(0, 6).map((opportunity, index) => (
                        <div
                            key={opportunity.product_id}
                            className="card animate-fade-in"
                            style={{ animationDelay: `${index * 0.1}s` }}
                        >
                            <h3 className="font-semibold mb-3 line-clamp-2">
                                {opportunity.product_name}
                            </h3>
                            <div className="space-y-2 text-sm">
                                <div className="flex justify-between">
                                    <span className="text-dark-muted">Prix AliExpress:</span>
                                    <span className="font-semibold">${opportunity.aliexpress_price}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-dark-muted">Prix Amazon:</span>
                                    <span className="font-semibold">${opportunity.amazon_price}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-dark-muted">Marge Nette:</span>
                                    <span className="font-semibold text-accent-success">
                                        ${opportunity.marge_nette?.toFixed(2)}
                                    </span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-dark-muted">ROI:</span>
                                    <span className="font-semibold text-accent-warning">
                                        {opportunity.roi_percentage?.toFixed(1)}%
                                    </span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Low Saturation Markets */}
            <div>
                <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                    <span>💎</span> Marchés Peu Saturés
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {summary?.low_saturation_markets?.slice(0, 8).map((market, index) => (
                        <div
                            key={market.product_id}
                            className="card animate-fade-in"
                            style={{ animationDelay: `${index * 0.1}s` }}
                        >
                            <h3 className="font-semibold mb-3 line-clamp-2 text-sm">
                                {market.product_name}
                            </h3>
                            <div className="space-y-2 text-xs">
                                <div className="flex justify-between">
                                    <span className="text-dark-muted">Concurrents:</span>
                                    <span className="font-semibold">{market.competitors_count}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-dark-muted">Saturation:</span>
                                    <span className="font-semibold">{market.saturation_score}%</span>
                                </div>
                                <div>
                                    <span
                                        className={`badge ${market.market_opportunity === 'high'
                                            ? 'badge-success'
                                            : market.market_opportunity === 'medium'
                                                ? 'badge-warning'
                                                : 'badge-danger'
                                            }`}
                                    >
                                        {market.market_opportunity}
                                    </span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Footer */}
            <footer className="mt-16 text-center text-dark-muted text-sm">
                <p>
                    Données mises à jour automatiquement • Scraping quotidien • Prix toutes les 6h
                </p>
            </footer>
        </div>
    )
}
