from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration Celery
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = Celery(
    'ecommerce_scraper',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        'tasks.scraping_tasks',
        'tasks.alert_tasks',
        'tasks.export_tasks'
    ]
)

# Configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 heure max par tâche
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
)

# Planification des tâches périodiques
app.conf.beat_schedule = {
    # Scraping quotidien à 2h du matin
    'scrape-all-sources-daily': {
        'task': 'tasks.scraping_tasks.scrape_all_sources',
        'schedule': crontab(hour=2, minute=0),
    },
    # Mise à jour des prix toutes les 6h
    'update-prices-6h': {
        'task': 'tasks.scraping_tasks.update_prices',
        'schedule': crontab(minute=0, hour='*/6'),
    },
    # Calcul des tendances quotidien à 3h du matin
    'calculate-trends-daily': {
        'task': 'tasks.scraping_tasks.calculate_trends',
        'schedule': crontab(hour=3, minute=0),
    },
    # Vérification des alertes toutes les heures
    'check-alerts-hourly': {
        'task': 'tasks.alert_tasks.check_alerts',
        'schedule': crontab(minute=0),
    },
    # Export hebdomadaire le dimanche à 23h
    'export-weekly-report': {
        'task': 'tasks.export_tasks.export_weekly_report',
        'schedule': crontab(hour=23, minute=0, day_of_week=0),
    },
}

if __name__ == '__main__':
    app.start()
