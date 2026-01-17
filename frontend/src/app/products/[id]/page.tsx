'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'

interface ProductDetail {
    id: number
    nom: string
    description: string
    categorie: string
    prix: number
    source: string
    rating: number
    reviews_count: number
    stock_status: string
    image_url: string
    url: string
    asin: string
}

interface PriceHistory {
    prix: number
    date: string
}

interface Trend {
    score_tendance: number
    volume_ventes_estime: number
    saturation_marche: number
    marge_beneficiaire: number
}

export default function ProductDetailPage() {
    const params = useParams()
    const [product, setProduct] = useState<ProductDetail | null>(null)
    const [priceHistory, setPriceHistory] = useState<PriceHistory[]>([])
    const [trend, setTrend] = useState<Trend | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (params.id) {
            fetchProductDetail()
        }
    }, [params.id])

    const fetchProductDetail = async () => {
        try {
            let apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

            if (typeof window !== 'undefined' && window.location.hostname.includes('app.github.dev')) {
                const baseUrl = window.location.origin.replace('-3000', '-8000')
                apiUrl = baseUrl
            }

            const response = await fetch(`${apiUrl}/api/products/${params.id}`)
            const data = await response.json()
            setProduct(data)

            // Fetch price history
            const historyResponse = await fetch(`${apiUrl}/api/products/${params.id}/price-history`)
            const historyData = await historyResponse.json()
            setPriceHistory(historyData)

            // Fetch trend data
            const trendResponse = await fetch(`${apiUrl}/api/analytics/product/${params.id}/trend`)
            const trendData = await trendResponse.json()
            setTrend(trendData)

        } catch (error) {
            console.error('Error fetching product detail:', error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-pulse-slow text-6xl mb-4">📦</div>
                    <p className="text-dark-muted">Chargement du produit...</p>
                </div>
            </div>
        )
    }

    if (!product) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="text-6xl mb-4">❌</div>
                    <p className="text-dark-muted">Produit non trouvé</p>
                    <Link href="/products" className="btn btn-primary mt-4">
                        Retour aux produits
                    </Link>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen p-8">
            <Link href="/products" className="text-accent-primary hover:underline mb-4 inline-block">
                ← Retour aux produits
            </Link>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                {/* Product Image */}
                <div className="card">
                    <img
                        src={product.image_url}
                        alt={product.nom}
                        className="w-full rounded-lg"
                    />
                </div>

                {/* Product Info */}
                <div>
                    <div className="mb-4">
                        <span className="badge badge-primary">{product.source}</span>
                        <span className="badge badge-secondary ml-2">{product.categorie}</span>
                    </div>

                    <h1 className="text-4xl font-bold mb-4">{product.nom}</h1>

                    <div className="flex items-center gap-4 mb-6">
                        <span className="text-5xl font-bold text-accent-success">
                            ${product.prix}
                        </span>
                        <div className="flex items-center gap-2">
                            <span className="text-2xl">⭐</span>
                            <span className="text-xl font-semibold">{product.rating}</span>
                            <span className="text-dark-muted">
                                ({product.reviews_count} avis)
                            </span>
                        </div>
                    </div>

                    <div className="mb-6">
                        <span className={`px-4 py-2 rounded-lg ${product.stock_status === 'In Stock'
                                ? 'bg-accent-success/20 text-accent-success'
                                : 'bg-accent-warning/20 text-accent-warning'
                            }`}>
                            {product.stock_status}
                        </span>
                    </div>

                    <p className="text-dark-muted mb-6">{product.description}</p>

                    <div className="space-y-2 mb-6">
                        <p><strong>ASIN:</strong> {product.asin}</p>
                        <p><strong>Source:</strong> {product.source}</p>
                        <p><strong>Catégorie:</strong> {product.categorie}</p>
                    </div>

                    <a
                        href={product.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-primary w-full text-center"
                    >
                        Voir sur {product.source} →
                    </a>
                </div>
            </div>

            {/* Trend Data */}
            {trend && (
                <div className="card mb-8">
                    <h2 className="text-2xl font-bold mb-6">📊 Analyse de Tendance</h2>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                        <div>
                            <div className="text-dark-muted text-sm mb-2">Score Tendance</div>
                            <div className="text-3xl font-bold text-accent-primary">
                                {trend.score_tendance}
                            </div>
                        </div>
                        <div>
                            <div className="text-dark-muted text-sm mb-2">Ventes Estimées</div>
                            <div className="text-3xl font-bold text-accent-success">
                                {trend.volume_ventes_estime}
                            </div>
                        </div>
                        <div>
                            <div className="text-dark-muted text-sm mb-2">Saturation Marché</div>
                            <div className="text-3xl font-bold text-accent-warning">
                                {trend.saturation_marche}%
                            </div>
                        </div>
                        <div>
                            <div className="text-dark-muted text-sm mb-2">Marge Bénéficiaire</div>
                            <div className="text-3xl font-bold text-accent-success">
                                ${trend.marge_beneficiaire}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Price History */}
            {priceHistory.length > 0 && (
                <div className="card">
                    <h2 className="text-2xl font-bold mb-6">💰 Historique des Prix</h2>
                    <div className="space-y-2">
                        {priceHistory.slice(0, 10).map((history, index) => (
                            <div key={index} className="flex justify-between items-center p-3 bg-dark-lighter rounded-lg">
                                <span className="text-dark-muted">
                                    {new Date(history.date).toLocaleDateString()}
                                </span>
                                <span className="font-semibold text-accent-success">
                                    ${history.prix}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}
