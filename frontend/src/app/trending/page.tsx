'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

interface TrendingProduct {
    id: number
    nom: string
    score: number
    prix: number
    source: string
    categorie: string
    image_url: string
}

export default function TrendingPage() {
    const [trending, setTrending] = useState<TrendingProduct[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchTrending()
    }, [])

    const fetchTrending = async () => {
        try {
            let apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

            if (typeof window !== 'undefined' && window.location.hostname.includes('app.github.dev')) {
                const baseUrl = window.location.origin.replace('-3000', '-8000')
                apiUrl = baseUrl
            }

            const response = await fetch(`${apiUrl}/api/analytics/trending`)
            const data = await response.json()
            setTrending(data)
        } catch (error) {
            console.error('Error fetching trending:', error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-pulse-slow text-6xl mb-4">🔥</div>
                    <p className="text-dark-muted">Chargement des tendances...</p>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen p-8">
            <header className="mb-12">
                <Link href="/" className="text-accent-primary hover:underline mb-4 inline-block">
                    ← Retour au dashboard
                </Link>
                <h1 className="text-5xl font-bold mb-2 bg-gradient-to-r from-accent-warning to-accent-danger bg-clip-text text-transparent">
                    🔥 Produits Tendances
                </h1>
                <p className="text-dark-muted text-lg">
                    {trending.length} produits en forte croissance
                </p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {trending.map((product, index) => (
                    <div
                        key={product.id}
                        className="card animate-fade-in hover:scale-105 transition-transform"
                        style={{ animationDelay: `${index * 0.05}s` }}
                    >
                        <div className="mb-4">
                            <img
                                src={product.image_url}
                                alt={product.nom}
                                className="w-full h-48 object-cover rounded-lg"
                            />
                        </div>

                        <div className="flex justify-between items-start mb-3">
                            <div>
                                <span className="badge badge-primary text-xs">
                                    {product.source}
                                </span>
                                <span className="badge badge-secondary text-xs ml-2">
                                    {product.categorie}
                                </span>
                            </div>
                            <span className="badge badge-warning text-lg font-bold">
                                🔥 {product.score}
                            </span>
                        </div>

                        <h3 className="font-semibold text-lg mb-3 line-clamp-2">
                            {product.nom}
                        </h3>

                        <div className="flex items-center justify-between mb-4">
                            <span className="text-2xl font-bold text-accent-success">
                                ${product.prix}
                            </span>
                        </div>

                        <Link
                            href={`/products/${product.id}`}
                            className="btn btn-primary w-full text-center"
                        >
                            Voir détails →
                        </Link>
                    </div>
                ))}
            </div>
        </div>
    )
}
