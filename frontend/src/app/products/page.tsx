'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

interface Product {
    id: number
    nom: string
    categorie: string
    prix: number
    source: string
    rating: number
    reviews_count: number
    stock_status: string
    image_url: string
}

export default function ProductsPage() {
    const [products, setProducts] = useState<Product[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchProducts()
    }, [])

    const fetchProducts = async () => {
        try {
            let apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

            if (typeof window !== 'undefined' && window.location.hostname.includes('app.github.dev')) {
                const baseUrl = window.location.origin.replace('-3000', '-8000')
                apiUrl = baseUrl
            }

            const response = await fetch(`${apiUrl}/api/products/`)
            const data = await response.json()
            setProducts(data)
        } catch (error) {
            console.error('Error fetching products:', error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-pulse-slow text-6xl mb-4">📦</div>
                    <p className="text-dark-muted">Chargement des produits...</p>
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
                <h1 className="text-5xl font-bold mb-2 bg-gradient-to-r from-accent-primary to-accent-success bg-clip-text text-transparent">
                    📦 Tous les Produits
                </h1>
                <p className="text-dark-muted text-lg">
                    {products.length} produits scrapés
                </p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {products.map((product, index) => (
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

                        <div className="mb-2">
                            <span className="badge badge-primary text-xs">
                                {product.source}
                            </span>
                            <span className="badge badge-secondary text-xs ml-2">
                                {product.categorie}
                            </span>
                        </div>

                        <h3 className="font-semibold text-lg mb-2 line-clamp-2">
                            {product.nom}
                        </h3>

                        <div className="flex items-center justify-between mb-3">
                            <span className="text-2xl font-bold text-accent-success">
                                ${product.prix}
                            </span>
                            <div className="flex items-center gap-1">
                                <span className="text-accent-warning">⭐</span>
                                <span className="text-sm">{product.rating}</span>
                                <span className="text-xs text-dark-muted">
                                    ({product.reviews_count})
                                </span>
                            </div>
                        </div>

                        <div className="mb-4">
                            <span className={`text-xs px-2 py-1 rounded ${product.stock_status === 'In Stock'
                                    ? 'bg-accent-success/20 text-accent-success'
                                    : 'bg-accent-warning/20 text-accent-warning'
                                }`}>
                                {product.stock_status}
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
