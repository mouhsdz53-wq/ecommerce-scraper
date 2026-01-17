import type { Metadata } from 'next'
import './globals.css'
import Navigation from '@/components/Navigation'

export const metadata: Metadata = {
    title: 'E-Commerce Scraper - Veille Produits Tendances',
    description: 'Plateforme de veille e-commerce pour identifier les produits tendances',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="fr" className="dark">
            <body>
                <Navigation />
                {children}
            </body>
        </html>
    )
}
