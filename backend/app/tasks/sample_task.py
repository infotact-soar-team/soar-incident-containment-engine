from app.core.celery_app import celery_app


@celery_app.task(name="sample_task")
def add(x: int, y: int) -> int:
    """Sanity-check task confirming Celery is wired up correctly."""
    return x + y