from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.triggers.cron import CronTrigger

from .scubscription import check_all_subscriptions_job

from app.config import settings


_job_stores = {
    'default': RedisJobStore(
        jobs_key='dispatched_jobs',
        run_times_key='dispatched_jobs_running',
        host=settings.redis_host,
        port=settings.redis_port
    )
}
scheduler = AsyncIOScheduler(jobstores=_job_stores)

scheduler.add_job(check_all_subscriptions_job, trigger=CronTrigger(hour=0))
