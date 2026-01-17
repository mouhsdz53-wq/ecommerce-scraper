'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

interface Alert {
    id: number
    product_id: number
    type_alerte: string
    seuil: number
    actif: boolean
    created_at: string
}

export default function AlertsPage() {
    const [alerts, setAlerts] = useState<Alert[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchAlerts()
    }, [])

    const fetchAlerts = async () => {
        try {
            let apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

            if (typeof window !== 'undefined' && window.location.hostname.includes('app.github.dev')) {
                const baseUrl = window.location.origin.replace('-3000', '-8000')
                apiUrl = baseUrl
            }

            const response = await fetch(`${apiUrl}/api/alerts/`)
            const data = await response.json()
            setAlerts(data)
        } catch (error) {
            console.error('Error fetching alerts:', error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-pulse-slow text-6xl mb-4">🔔</div>
                    <p className="text-dark-muted">Chargement des alertes...</p>
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
                    🔔 Alertes
                </h1>
                <p className="text-dark-muted text-lg">
                    {alerts.length} alertes configurées
                </p>
            </header>

            {alerts.length === 0 ? (
                <div className="card text-center py-12">
                    <div className="text-6xl mb-4">🔕</div>
                    <h2 className="text-2xl font-bold mb-2">Aucune alerte configurée</h2>
                    <p className="text-dark-muted mb-6">
                        Créez des alertes pour être notifié des changements de prix et des opportunités
                    </p>
                    <button className="btn btn-primary">
                        Créer une alerte
                    </button>
                </div>
            ) : (
                <div className="space-y-4">
                    {alerts.map((alert, index) => (
                        <div
                            key={alert.id}
                            className="card animate-fade-in"
                            style={{ animationDelay: `${index * 0.05}s` }}
                        >
                            <div className="flex justify-between items-center">
                                <div>
                                    <h3 className="font-semibold text-lg mb-2">
                                        {alert.type_alerte}
                                    </h3>
                                    <p className="text-dark-muted text-sm">
                                        Seuil: ${alert.seuil} • Créée le {new Date(alert.created_at).toLocaleDateString()}
                                    </p>
                                </div>
                                <div className="flex items-center gap-4">
                                    <span className={`badge ${alert.actif ? 'badge-success' : 'badge-danger'}`}>
                                        {alert.actif ? 'Active' : 'Inactive'}
                                    </span>
                                    <Link
                                        href={`/products/${alert.product_id}`}
                                        className="btn btn-secondary"
                                    >
                                        Voir produit
                                    </Link>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
