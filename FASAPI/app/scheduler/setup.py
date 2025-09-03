"""
Scheduler setup and job configuration.
"""
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import settings
from app.core.logging import logger
from app.jobs.cleaners import (
    cleanup_expired_cache,
    cleanup_old_logs,
    health_check_external_sources,
)

# Global scheduler instance
scheduler: AsyncIOScheduler = None


def setup_scheduler():
    """Set up and start the job scheduler."""
    
    global scheduler
    
    if not settings.SCHEDULER_ENABLED:
        logger.info("Scheduler is disabled")
        return
    
    logger.info("Setting up job scheduler")
    
    # Create scheduler
    scheduler = AsyncIOScheduler()
    
    # Add jobs
    _add_cleanup_jobs()
    _add_monitoring_jobs()
    
    # Start scheduler
    scheduler.start()
    logger.info("Job scheduler started")


def _add_cleanup_jobs():
    """Add cleanup jobs to the scheduler."""
    
    # Cache cleanup - every hour
    scheduler.add_job(
        cleanup_expired_cache,
        trigger=IntervalTrigger(hours=1),
        id="cleanup_cache",
        name="Cleanup expired cache entries",
        replace_existing=True,
    )
    
    # Log cleanup - daily at 2 AM
    scheduler.add_job(
        cleanup_old_logs,
        trigger=CronTrigger(hour=2, minute=0),
        id="cleanup_logs",
        name="Cleanup old log files",
        replace_existing=True,
    )
    
    logger.info("Added cleanup jobs to scheduler")


def _add_monitoring_jobs():
    """Add monitoring jobs to the scheduler."""
    
    # External sources health check - every 30 minutes
    scheduler.add_job(
        health_check_external_sources,
        trigger=IntervalTrigger(minutes=30),
        id="health_check_sources",
        name="Health check external sources",
        replace_existing=True,
    )
    
    logger.info("Added monitoring jobs to scheduler")


def shutdown_scheduler():
    """Shutdown the job scheduler."""
    
    global scheduler
    
    if scheduler and scheduler.running:
        logger.info("Shutting down job scheduler")
        scheduler.shutdown(wait=True)
        logger.info("Job scheduler shut down")


def get_scheduler_status():
    """Get scheduler status and job information."""
    
    if not scheduler:
        return {"status": "not_initialized"}
    
    if not scheduler.running:
        return {"status": "stopped"}
    
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
            "trigger": str(job.trigger),
        })
    
    return {
        "status": "running",
        "jobs": jobs,
        "job_count": len(jobs),
    }