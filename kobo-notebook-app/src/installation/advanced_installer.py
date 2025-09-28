"""
Advanced installation system with batch operations and scheduling.

This module provides enhanced installation capabilities including batch
operations, installation scheduling, and advanced device management.
"""

import os
import json
import time
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from utils.logger import setup_logger
from installation.kobo_installer import KoboInstaller


class InstallationStatus(Enum):
    """Installation status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class InstallationJob:
    """Represents an installation job."""
    id: str
    name: str
    templates: List[str]
    device_path: str
    status: InstallationStatus
    created: datetime
    scheduled: Optional[datetime] = None
    started: Optional[datetime] = None
    completed: Optional[datetime] = None
    error_message: Optional[str] = None
    progress: float = 0.0


class AdvancedInstaller:
    """Advanced installer with batch operations and scheduling."""
    
    def __init__(self):
        """Initialize the advanced installer."""
        self.logger = setup_logger()
        self.installer = KoboInstaller()
        self.jobs: Dict[str, InstallationJob] = {}
        self.job_queue: List[str] = []
        self.current_job: Optional[str] = None
        self.worker_thread: Optional[threading.Thread] = None
        self.stop_worker = False
        self.progress_callbacks: List[Callable] = []
        
        # Load existing jobs
        self.load_jobs()
        
        # Start worker thread
        self.start_worker()
    
    def create_installation_job(
        self,
        name: str,
        templates: List[str],
        device_path: str,
        scheduled_time: Optional[datetime] = None
    ) -> str:
        """
        Create a new installation job.
        
        Args:
            name (str): Job name
            templates (List[str]): List of template paths
            device_path (str): Target device path
            scheduled_time (Optional[datetime]): When to run the job
            
        Returns:
            str: Job ID
        """
        try:
            job_id = f"job_{int(time.time())}_{len(self.jobs)}"
            
            job = InstallationJob(
                id=job_id,
                name=name,
                templates=templates,
                device_path=device_path,
                status=InstallationStatus.PENDING,
                created=datetime.now(),
                scheduled=scheduled_time
            )
            
            self.jobs[job_id] = job
            self.job_queue.append(job_id)
            
            # Save jobs
            self.save_jobs()
            
            self.logger.info(f"Created installation job: {job_id}")
            return job_id
            
        except Exception as e:
            self.logger.error(f"Error creating installation job: {e}")
            raise
    
    def get_job_status(self, job_id: str) -> Optional[InstallationJob]:
        """
        Get the status of an installation job.
        
        Args:
            job_id (str): Job ID
            
        Returns:
            Optional[InstallationJob]: Job information
        """
        return self.jobs.get(job_id)
    
    def list_jobs(self, status_filter: Optional[InstallationStatus] = None) -> List[InstallationJob]:
        """
        List installation jobs.
        
        Args:
            status_filter (Optional[InstallationStatus]): Filter by status
            
        Returns:
            List[InstallationJob]: List of jobs
        """
        jobs = list(self.jobs.values())
        
        if status_filter:
            jobs = [job for job in jobs if job.status == status_filter]
        
        # Sort by creation time (newest first)
        jobs.sort(key=lambda x: x.created, reverse=True)
        
        return jobs
    
    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel an installation job.
        
        Args:
            job_id (str): Job ID to cancel
            
        Returns:
            bool: True if job was cancelled
        """
        try:
            if job_id not in self.jobs:
                return False
            
            job = self.jobs[job_id]
            
            if job.status == InstallationStatus.IN_PROGRESS:
                # Mark for cancellation
                job.status = InstallationStatus.CANCELLED
                self.logger.info(f"Marked job for cancellation: {job_id}")
            elif job.status == InstallationStatus.PENDING:
                # Remove from queue
                job.status = InstallationStatus.CANCELLED
                if job_id in self.job_queue:
                    self.job_queue.remove(job_id)
                self.logger.info(f"Cancelled pending job: {job_id}")
            else:
                self.logger.warning(f"Cannot cancel job in status: {job.status}")
                return False
            
            self.save_jobs()
            return True
            
        except Exception as e:
            self.logger.error(f"Error cancelling job {job_id}: {e}")
            return False
    
    def delete_job(self, job_id: str) -> bool:
        """
        Delete an installation job.
        
        Args:
            job_id (str): Job ID to delete
            
        Returns:
            bool: True if job was deleted
        """
        try:
            if job_id not in self.jobs:
                return False
            
            job = self.jobs[job_id]
            
            # Only delete completed, failed, or cancelled jobs
            if job.status in [InstallationStatus.COMPLETED, InstallationStatus.FAILED, InstallationStatus.CANCELLED]:
                del self.jobs[job_id]
                if job_id in self.job_queue:
                    self.job_queue.remove(job_id)
                
                self.save_jobs()
                self.logger.info(f"Deleted job: {job_id}")
                return True
            else:
                self.logger.warning(f"Cannot delete job in status: {job.status}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error deleting job {job_id}: {e}")
            return False
    
    def install_batch(self, job_ids: List[str]) -> Dict[str, bool]:
        """
        Install multiple jobs in batch.
        
        Args:
            job_ids (List[str]): List of job IDs to install
            
        Returns:
            Dict[str, bool]: Results for each job
        """
        results = {}
        
        try:
            for job_id in job_ids:
                if job_id in self.jobs:
                    job = self.jobs[job_id]
                    if job.status == InstallationStatus.PENDING:
                        # Add to queue if not already there
                        if job_id not in self.job_queue:
                            self.job_queue.append(job_id)
                        results[job_id] = True
                    else:
                        results[job_id] = False
                else:
                    results[job_id] = False
            
            self.logger.info(f"Queued {len([r for r in results.values() if r])} jobs for batch installation")
            
        except Exception as e:
            self.logger.error(f"Error in batch installation: {e}")
        
        return results
    
    def start_worker(self):
        """Start the worker thread for processing jobs."""
        if self.worker_thread and self.worker_thread.is_alive():
            return
        
        self.stop_worker = False
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        
        self.logger.info("Started installation worker thread")
    
    def stop_worker_thread(self):
        """Stop the worker thread."""
        self.stop_worker = True
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=5)
        
        self.logger.info("Stopped installation worker thread")
    
    def _worker_loop(self):
        """Worker thread main loop."""
        while not self.stop_worker:
            try:
                # Check for jobs to process
                if self.job_queue and not self.current_job:
                    job_id = self.job_queue.pop(0)
                    self._process_job(job_id)
                
                # Sleep briefly to avoid busy waiting
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error in worker loop: {e}")
                time.sleep(5)  # Wait longer on error
    
    def _process_job(self, job_id: str):
        """Process a single installation job."""
        try:
            if job_id not in self.jobs:
                return
            
            job = self.jobs[job_id]
            
            # Check if job is scheduled for later
            if job.scheduled and job.scheduled > datetime.now():
                # Put back in queue
                self.job_queue.insert(0, job_id)
                return
            
            # Check if job was cancelled
            if job.status == InstallationStatus.CANCELLED:
                return
            
            # Start job
            job.status = InstallationStatus.IN_PROGRESS
            job.started = datetime.now()
            job.progress = 0.0
            self.current_job = job_id
            
            self.logger.info(f"Starting installation job: {job_id}")
            self._notify_progress(job_id, 0.0, "Starting installation...")
            
            # Create installation package
            self._notify_progress(job_id, 10.0, "Creating installation package...")
            package_path = self.installer.create_installation_package(
                templates=job.templates,
                output_path=str(Path.home() / ".kobo_notebook_app" / "temp"),
                package_name=f"batch_install_{job_id}"
            )
            
            # Install package
            self._notify_progress(job_id, 50.0, "Installing package...")
            success = self.installer.install_package(package_path, job.device_path)
            
            if success:
                job.status = InstallationStatus.COMPLETED
                job.progress = 100.0
                job.completed = datetime.now()
                self._notify_progress(job_id, 100.0, "Installation completed successfully")
                self.logger.info(f"Completed installation job: {job_id}")
            else:
                job.status = InstallationStatus.FAILED
                job.error_message = "Installation failed"
                self._notify_progress(job_id, 0.0, "Installation failed")
                self.logger.error(f"Failed installation job: {job_id}")
            
            # Clean up
            try:
                os.remove(package_path)
            except:
                pass
            
            # Save jobs
            self.save_jobs()
            
        except Exception as e:
            if job_id in self.jobs:
                job = self.jobs[job_id]
                job.status = InstallationStatus.FAILED
                job.error_message = str(e)
                self._notify_progress(job_id, 0.0, f"Error: {e}")
            
            self.logger.error(f"Error processing job {job_id}: {e}")
        
        finally:
            self.current_job = None
    
    def _notify_progress(self, job_id: str, progress: float, message: str):
        """Notify progress callbacks."""
        for callback in self.progress_callbacks:
            try:
                callback(job_id, progress, message)
            except Exception as e:
                self.logger.error(f"Error in progress callback: {e}")
    
    def add_progress_callback(self, callback: Callable):
        """Add a progress callback function."""
        self.progress_callbacks.append(callback)
    
    def remove_progress_callback(self, callback: Callable):
        """Remove a progress callback function."""
        if callback in self.progress_callbacks:
            self.progress_callbacks.remove(callback)
    
    def save_jobs(self):
        """Save jobs to disk."""
        try:
            jobs_dir = Path.home() / ".kobo_notebook_app" / "jobs"
            jobs_dir.mkdir(parents=True, exist_ok=True)
            
            jobs_file = jobs_dir / "installation_jobs.json"
            
            # Convert jobs to serializable format
            jobs_data = {}
            for job_id, job in self.jobs.items():
                jobs_data[job_id] = {
                    "id": job.id,
                    "name": job.name,
                    "templates": job.templates,
                    "device_path": job.device_path,
                    "status": job.status.value,
                    "created": job.created.isoformat(),
                    "scheduled": job.scheduled.isoformat() if job.scheduled else None,
                    "started": job.started.isoformat() if job.started else None,
                    "completed": job.completed.isoformat() if job.completed else None,
                    "error_message": job.error_message,
                    "progress": job.progress
                }
            
            with open(jobs_file, 'w') as f:
                json.dump(jobs_data, f, indent=2)
            
        except Exception as e:
            self.logger.error(f"Error saving jobs: {e}")
    
    def load_jobs(self):
        """Load jobs from disk."""
        try:
            jobs_dir = Path.home() / ".kobo_notebook_app" / "jobs"
            jobs_file = jobs_dir / "installation_jobs.json"
            
            if not jobs_file.exists():
                return
            
            with open(jobs_file, 'r') as f:
                jobs_data = json.load(f)
            
            for job_id, job_data in jobs_data.items():
                job = InstallationJob(
                    id=job_data["id"],
                    name=job_data["name"],
                    templates=job_data["templates"],
                    device_path=job_data["device_path"],
                    status=InstallationStatus(job_data["status"]),
                    created=datetime.fromisoformat(job_data["created"]),
                    scheduled=datetime.fromisoformat(job_data["scheduled"]) if job_data["scheduled"] else None,
                    started=datetime.fromisoformat(job_data["started"]) if job_data["started"] else None,
                    completed=datetime.fromisoformat(job_data["completed"]) if job_data["completed"] else None,
                    error_message=job_data["error_message"],
                    progress=job_data["progress"]
                )
                
                self.jobs[job_id] = job
                
                # Add pending jobs to queue
                if job.status == InstallationStatus.PENDING:
                    self.job_queue.append(job_id)
            
            self.logger.info(f"Loaded {len(self.jobs)} installation jobs")
            
        except Exception as e:
            self.logger.error(f"Error loading jobs: {e}")
    
    def get_installation_statistics(self) -> Dict[str, Any]:
        """Get installation statistics."""
        stats = {
            "total_jobs": len(self.jobs),
            "pending_jobs": len([j for j in self.jobs.values() if j.status == InstallationStatus.PENDING]),
            "in_progress_jobs": len([j for j in self.jobs.values() if j.status == InstallationStatus.IN_PROGRESS]),
            "completed_jobs": len([j for j in self.jobs.values() if j.status == InstallationStatus.COMPLETED]),
            "failed_jobs": len([j for j in self.jobs.values() if j.status == InstallationStatus.FAILED]),
            "cancelled_jobs": len([j for j in self.jobs.values() if j.status == InstallationStatus.CANCELLED]),
            "queue_length": len(self.job_queue),
            "current_job": self.current_job
        }
        
        # Calculate success rate
        total_processed = stats["completed_jobs"] + stats["failed_jobs"]
        if total_processed > 0:
            stats["success_rate"] = stats["completed_jobs"] / total_processed
        else:
            stats["success_rate"] = 0.0
        
        return stats
    
    def cleanup_old_jobs(self, days_old: int = 30):
        """Clean up old completed/failed jobs."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            jobs_to_remove = []
            
            for job_id, job in self.jobs.items():
                if (job.status in [InstallationStatus.COMPLETED, InstallationStatus.FAILED] and
                    job.completed and job.completed < cutoff_date):
                    jobs_to_remove.append(job_id)
            
            for job_id in jobs_to_remove:
                del self.jobs[job_id]
                if job_id in self.job_queue:
                    self.job_queue.remove(job_id)
            
            if jobs_to_remove:
                self.save_jobs()
                self.logger.info(f"Cleaned up {len(jobs_to_remove)} old jobs")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up old jobs: {e}")