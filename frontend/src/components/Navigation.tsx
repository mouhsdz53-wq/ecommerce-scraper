'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState } from 'react'

export default function Navigation() {
    const pathname = usePathname()
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

    const navItems = [
        { href: '/', label: '🏠 Dashboard', icon: '📊' },
        { href: '/products', label: '📦 Produits', icon: '📦' },
        { href: '/trending', label: '🔥 Tendances', icon: '🔥' },
        { href: '/analytics', label: '📊 Analytics', icon: '📊' },
        { href: '/alerts', label: '🔔 Alertes', icon: '🔔' },
    ]

    const isActive = (href: string) => {
        if (href === '/') return pathname === '/'
        return pathname.startsWith(href)
    }

    return (
        <nav className="sticky top-0 z-50 bg-dark-card/95 backdrop-blur-lg border-b border-dark-lighter shadow-lg">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link href="/" className="flex items-center space-x-3 group">
                        <div className="text-3xl group-hover:scale-110 transition-transform">
                            🛒
                        </div>
                        <div>
                            <h1 className="text-xl font-bold bg-gradient-to-r from-accent-primary to-accent-success bg-clip-text text-transparent">
                                E-Commerce Scraper
                            </h1>
                            <p className="text-xs text-dark-muted">Intelligence Platform</p>
                        </div>
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center space-x-1">
                        {navItems.map((item) => (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={`
                                    px-4 py-2 rounded-lg font-medium transition-all duration-200
                                    ${isActive(item.href)
                                        ? 'bg-accent-primary text-white shadow-lg shadow-accent-primary/50'
                                        : 'text-dark-muted hover:text-white hover:bg-dark-lighter'
                                    }
                                `}
                            >
                                <span className="flex items-center gap-2">
                                    <span>{item.icon}</span>
                                    <span className="hidden lg:inline">{item.label.split(' ')[1]}</span>
                                </span>
                            </Link>
                        ))}
                    </div>

                    {/* Mobile menu button */}
                    <button
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        className="md:hidden p-2 rounded-lg hover:bg-dark-lighter transition-colors"
                    >
                        <svg
                            className="w-6 h-6"
                            fill="none"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="2"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            {mobileMenuOpen ? (
                                <path d="M6 18L18 6M6 6l12 12" />
                            ) : (
                                <path d="M4 6h16M4 12h16M4 18h16" />
                            )}
                        </svg>
                    </button>
                </div>
            </div>

            {/* Mobile Navigation */}
            {mobileMenuOpen && (
                <div className="md:hidden border-t border-dark-lighter animate-fade-in">
                    <div className="px-2 pt-2 pb-3 space-y-1">
                        {navItems.map((item) => (
                            <Link
                                key={item.href}
                                href={item.href}
                                onClick={() => setMobileMenuOpen(false)}
                                className={`
                                    block px-3 py-2 rounded-lg font-medium transition-all
                                    ${isActive(item.href)
                                        ? 'bg-accent-primary text-white'
                                        : 'text-dark-muted hover:text-white hover:bg-dark-lighter'
                                    }
                                `}
                            >
                                {item.label}
                            </Link>
                        ))}
                    </div>
                </div>
            )}
        </nav>
    )
}
