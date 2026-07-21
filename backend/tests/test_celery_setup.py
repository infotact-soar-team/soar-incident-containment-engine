from app.core.celery_app import celery_app
from app.tasks.sample_task import add


def test_celery_app_configured():
    assert celery_app.conf.broker_url is not None
    assert celery_app.conf.task_serializer == "json"


def test_sample_task_runs_synchronously():
    # .run() executes the task function directly without needing a live worker/broker
    result = add.run(2, 3)
    assert result == 5