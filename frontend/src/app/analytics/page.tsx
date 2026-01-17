'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

interface Analytics {
    total_products: number
    avg_price: number
    total_reviews: number
    categories: { categorie: string; count: number }[]
    sources: { source: string; count: number }[]
}

export default function AnalyticsPage() {
    const [analytics, setAnalytics] = useState<Analytics | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchAnalytics()
    }, [])

    const fetchAnalytics = async () => {
        try {
            let apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

            if (typeof window !== 'undefined' && window.location.hostname.includes('app.github.dev')) {
                const baseUrl = window.location.origin.replace('-3000', '-8000')
                apiUrl = baseUrl
            }

            const response = await fetch(`${apiUrl}/api/analytics/stats`)
            const data = await response.json()
            setAnalytics(data)
        } catch (error) {
            console.error('Error fetching analytics:', error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-pulse-slow text-6xl mb-4">📊</div>
                    <p className="text-dark-muted">Chargement des analytics...</p>
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
                <h1 className="text-5xl font-bold mb-2 bg-gradient-to-r from-accent-primary to-accent-info bg-clip-text text-transparent">
                    📊 Analytics
                </h1>
                <p className="text-dark-muted text-lg">
                    Vue d'ensemble des données scrapées
                </p>
            </header>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                <div className="card">
                    <div className="text-dark-muted text-sm mb-2">Total Produits</div>
                    <div className="text-4xl font-bold text-accent-primary">
                        {analytics?.total_products || 0}
                    </div>
                </div>

                <div className="card">
                    <div className="text-dark-muted text-sm mb-2">Prix Moyen</div>
                    <div className="text-4xl font-bold text-accent-success">
                        ${analytics?.avg_price?.toFixed(2) || 0}
                    </div>
                </div>

                <div className="card">
                    <div className="text-dark-muted text-sm mb-2">Total Avis</div>
                    <div className="text-4xl font-bold text-accent-warning">
                        {analytics?.total_reviews || 0}
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Categories */}
                <div className="card">
                    <h2 className="text-2xl font-bold mb-6">📦 Par Catégorie</h2>
                    <div className="space-y-3">
                        {analytics?.categories?.map((cat, index) => (
                            <div key={index} className="flex justify-between items-center p-3 bg-dark-lighter rounded-lg">
                                <span className="font-semibold">{cat.categorie}</span>
                                <span className="badge badge-primary">{cat.count} produits</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Sources */}
                <div className="card">
                    <h2 className="text-2xl font-bold mb-6">🌐 Par Source</h2>
                    <div className="space-y-3">
                        {analytics?.sources?.map((src, index) => (
                            <div key={index} className="flex justify-between items-center p-3 bg-dark-lighter rounded-lg">
                                <span className="font-semibold">{src.source}</span>
                                <span className="badge badge-success">{src.count} produits</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}
