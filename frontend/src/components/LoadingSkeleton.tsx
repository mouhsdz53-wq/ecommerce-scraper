export default function LoadingSkeleton({ type = 'card' }: { type?: 'card' | 'list' | 'detail' }) {
    if (type === 'card') {
        return (
            <div className="card animate-pulse">
                <div className="bg-dark-lighter h-48 rounded-lg mb-4"></div>
                <div className="space-y-3">
                    <div className="h-4 bg-dark-lighter rounded w-3/4"></div>
                    <div className="h-4 bg-dark-lighter rounded w-1/2"></div>
                    <div className="flex justify-between">
                        <div className="h-6 bg-dark-lighter rounded w-1/4"></div>
                        <div className="h-6 bg-dark-lighter rounded w-1/4"></div>
                    </div>
                </div>
            </div>
        )
    }

    if (type === 'list') {
        return (
            <div className="space-y-4">
                {[1, 2, 3, 4, 5].map((i) => (
                    <div key={i} className="card animate-pulse">
                        <div className="flex gap-4">
                            <div className="bg-dark-lighter h-24 w-24 rounded-lg flex-shrink-0"></div>
                            <div className="flex-1 space-y-3">
                                <div className="h-4 bg-dark-lighter rounded w-3/4"></div>
                                <div className="h-4 bg-dark-lighter rounded w-1/2"></div>
                                <div className="h-4 bg-dark-lighter rounded w-1/4"></div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        )
    }

    if (type === 'detail') {
        return (
            <div className="animate-pulse">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                    <div className="bg-dark-lighter h-96 rounded-lg"></div>
                    <div className="space-y-4">
                        <div className="h-8 bg-dark-lighter rounded w-3/4"></div>
                        <div className="h-6 bg-dark-lighter rounded w-1/2"></div>
                        <div className="h-4 bg-dark-lighter rounded w-full"></div>
                        <div className="h-4 bg-dark-lighter rounded w-full"></div>
                        <div className="h-4 bg-dark-lighter rounded w-2/3"></div>
                    </div>
                </div>
            </div>
        )
    }

    return null
}
