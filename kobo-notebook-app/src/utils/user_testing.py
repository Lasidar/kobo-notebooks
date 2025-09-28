#!/usr/bin/env python3
"""
User Testing Framework for Kobo Notebook App

This module provides tools for conducting user testing sessions,
gathering feedback, and analyzing user experience metrics.
"""

import os
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

from .logger import setup_logger


@dataclass
class UserTestSession:
    """Represents a user testing session."""
    session_id: str
    user_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    tasks_completed: List[str] = None
    feedback: Dict[str, Any] = None
    satisfaction_score: Optional[int] = None
    issues_encountered: List[str] = None
    suggestions: List[str] = None
    
    def __post_init__(self):
        if self.tasks_completed is None:
            self.tasks_completed = []
        if self.feedback is None:
            self.feedback = {}
        if self.issues_encountered is None:
            self.issues_encountered = []
        if self.suggestions is None:
            self.suggestions = []


@dataclass
class UserTestTask:
    """Represents a task in a user testing session."""
    task_id: str
    task_name: str
    description: str
    expected_outcome: str
    difficulty_level: str  # "easy", "medium", "hard"
    time_limit: Optional[int] = None  # seconds
    prerequisites: List[str] = None
    
    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = []


class UserTestingFramework:
    """Framework for conducting user testing sessions."""
    
    def __init__(self):
        self.logger = setup_logger()
        self.sessions: List[UserTestSession] = []
        self.tasks: List[UserTestTask] = []
        self._initialize_default_tasks()
    
    def _initialize_default_tasks(self):
        """Initialize default testing tasks."""
        self.tasks = [
            UserTestTask(
                task_id="device_detection",
                task_name="Device Detection",
                description="Connect your Kobo Elipsa 2e device and verify the app detects it",
                expected_outcome="Device appears in the device list with correct information",
                difficulty_level="easy",
                time_limit=120
            ),
            UserTestTask(
                task_id="template_generation",
                task_name="Template Generation",
                description="Create a lined notebook template with 7mm spacing",
                expected_outcome="Template is generated and saved successfully",
                difficulty_level="easy",
                time_limit=180,
                prerequisites=["device_detection"]
            ),
            UserTestTask(
                task_id="template_preview",
                task_name="Template Preview",
                description="Preview the generated template before saving",
                expected_outcome="Template preview window opens showing the template",
                difficulty_level="easy",
                time_limit=60,
                prerequisites=["template_generation"]
            ),
            UserTestTask(
                task_id="package_creation",
                task_name="Installation Package Creation",
                description="Create an installation package with 3 templates",
                expected_outcome="Package is created and validated successfully",
                difficulty_level="medium",
                time_limit=300,
                prerequisites=["template_generation"]
            ),
            UserTestTask(
                task_id="device_backup",
                task_name="Device Backup",
                description="Create a backup of your device before installation",
                expected_outcome="Backup is created successfully",
                difficulty_level="medium",
                time_limit=600,
                prerequisites=["device_detection"]
            ),
            UserTestTask(
                task_id="template_installation",
                task_name="Template Installation",
                description="Install custom templates to your device",
                expected_outcome="Templates are installed and appear in device",
                difficulty_level="hard",
                time_limit=900,
                prerequisites=["package_creation", "device_backup"]
            ),
            UserTestTask(
                task_id="template_library",
                task_name="Template Library Management",
                description="Import and organize templates in the library",
                expected_outcome="Templates are organized and categorized properly",
                difficulty_level="medium",
                time_limit=240
            ),
            UserTestTask(
                task_id="advanced_features",
                task_name="Advanced Features",
                description="Use advanced features like batch operations or scheduling",
                expected_outcome="Advanced features work as expected",
                difficulty_level="hard",
                time_limit=600,
                prerequisites=["template_generation"]
            )
        ]
    
    def create_test_session(self, user_id: str) -> UserTestSession:
        """Create a new user testing session."""
        session_id = f"session_{int(time.time())}_{user_id}"
        session = UserTestSession(
            session_id=session_id,
            user_id=user_id,
            start_time=datetime.now()
        )
        self.sessions.append(session)
        
        self.logger.info(f"Created user testing session: {session_id}")
        return session
    
    def get_available_tasks(self, session: UserTestSession) -> List[UserTestTask]:
        """Get tasks available for a given session."""
        completed_tasks = set(session.tasks_completed)
        
        available_tasks = []
        for task in self.tasks:
            # Check if all prerequisites are met
            prerequisites_met = all(
                prereq in completed_tasks for prereq in task.prerequisites
            )
            
            if prerequisites_met and task.task_id not in completed_tasks:
                available_tasks.append(task)
        
        return available_tasks
    
    def start_task(self, session: UserTestSession, task_id: str) -> bool:
        """Start a task in a session."""
        task = next((t for t in self.tasks if t.task_id == task_id), None)
        if not task:
            self.logger.error(f"Task not found: {task_id}")
            return False
        
        # Check prerequisites
        available_tasks = self.get_available_tasks(session)
        if task not in available_tasks:
            self.logger.error(f"Task {task_id} not available for session {session.session_id}")
            return False
        
        self.logger.info(f"Started task {task_id} in session {session.session_id}")
        return True
    
    def complete_task(self, session: UserTestSession, task_id: str, 
                     success: bool, notes: str = "") -> None:
        """Mark a task as completed."""
        if task_id not in session.tasks_completed:
            session.tasks_completed.append(task_id)
            
            # Add to feedback
            if "task_results" not in session.feedback:
                session.feedback["task_results"] = {}
            
            session.feedback["task_results"][task_id] = {
                "success": success,
                "notes": notes,
                "completion_time": datetime.now().isoformat()
            }
            
            self.logger.info(f"Completed task {task_id} in session {session.session_id}: {'Success' if success else 'Failed'}")
    
    def record_issue(self, session: UserTestSession, issue: str) -> None:
        """Record an issue encountered during testing."""
        session.issues_encountered.append(issue)
        self.logger.info(f"Recorded issue in session {session.session_id}: {issue}")
    
    def record_suggestion(self, session: UserTestSession, suggestion: str) -> None:
        """Record a user suggestion."""
        session.suggestions.append(suggestion)
        self.logger.info(f"Recorded suggestion in session {session.session_id}: {suggestion}")
    
    def add_feedback(self, session: UserTestSession, category: str, feedback: Any) -> None:
        """Add feedback to a session."""
        session.feedback[category] = feedback
        self.logger.info(f"Added {category} feedback to session {session.session_id}")
    
    def set_satisfaction_score(self, session: UserTestSession, score: int) -> None:
        """Set the user satisfaction score (1-5)."""
        if 1 <= score <= 5:
            session.satisfaction_score = score
            self.logger.info(f"Set satisfaction score {score} for session {session.session_id}")
        else:
            self.logger.error(f"Invalid satisfaction score: {score}. Must be 1-5.")
    
    def end_session(self, session: UserTestSession) -> None:
        """End a user testing session."""
        session.end_time = datetime.now()
        self.logger.info(f"Ended user testing session: {session.session_id}")
    
    def generate_session_report(self, session: UserTestSession) -> Dict[str, Any]:
        """Generate a detailed report for a session."""
        duration = None
        if session.end_time:
            duration = (session.end_time - session.start_time).total_seconds()
        
        # Calculate task success rate
        task_results = session.feedback.get("task_results", {})
        total_tasks = len(task_results)
        successful_tasks = sum(1 for result in task_results.values() if result.get("success", False))
        success_rate = (successful_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "start_time": session.start_time.isoformat(),
            "end_time": session.end_time.isoformat() if session.end_time else None,
            "duration_seconds": duration,
            "tasks_completed": session.tasks_completed,
            "task_success_rate": success_rate,
            "satisfaction_score": session.satisfaction_score,
            "issues_encountered": session.issues_encountered,
            "suggestions": session.suggestions,
            "feedback": session.feedback
        }
    
    def generate_overall_report(self) -> Dict[str, Any]:
        """Generate an overall report for all sessions."""
        if not self.sessions:
            return {"error": "No sessions found"}
        
        completed_sessions = [s for s in self.sessions if s.end_time]
        
        # Calculate overall metrics
        total_sessions = len(completed_sessions)
        avg_satisfaction = 0
        total_issues = 0
        total_suggestions = 0
        
        if completed_sessions:
            satisfaction_scores = [s.satisfaction_score for s in completed_sessions if s.satisfaction_score]
            avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else 0
            
            total_issues = sum(len(s.issues_encountered) for s in completed_sessions)
            total_suggestions = sum(len(s.suggestions) for s in completed_sessions)
        
        # Analyze common issues
        all_issues = []
        for session in completed_sessions:
            all_issues.extend(session.issues_encountered)
        
        issue_frequency = {}
        for issue in all_issues:
            issue_frequency[issue] = issue_frequency.get(issue, 0) + 1
        
        # Analyze common suggestions
        all_suggestions = []
        for session in completed_sessions:
            all_suggestions.extend(session.suggestions)
        
        suggestion_frequency = {}
        for suggestion in all_suggestions:
            suggestion_frequency[suggestion] = suggestion_frequency.get(suggestion, 0) + 1
        
        # Calculate task success rates
        task_success_rates = {}
        for task in self.tasks:
            task_results = []
            for session in completed_sessions:
                task_result = session.feedback.get("task_results", {}).get(task.task_id)
                if task_result:
                    task_results.append(task_result.get("success", False))
            
            if task_results:
                task_success_rates[task.task_id] = sum(task_results) / len(task_results) * 100
        
        return {
            "report_generated": datetime.now().isoformat(),
            "total_sessions": total_sessions,
            "average_satisfaction_score": round(avg_satisfaction, 2),
            "total_issues": total_issues,
            "total_suggestions": total_suggestions,
            "common_issues": sorted(issue_frequency.items(), key=lambda x: x[1], reverse=True),
            "common_suggestions": sorted(suggestion_frequency.items(), key=lambda x: x[1], reverse=True),
            "task_success_rates": task_success_rates,
            "session_reports": [self.generate_session_report(s) for s in completed_sessions]
        }
    
    def save_sessions(self, filepath: str) -> None:
        """Save all sessions to file."""
        try:
            sessions_data = [asdict(session) for session in self.sessions]
            with open(filepath, 'w') as f:
                json.dump(sessions_data, f, indent=2, default=str)
            self.logger.info(f"Saved {len(self.sessions)} sessions to {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save sessions: {e}")
    
    def load_sessions(self, filepath: str) -> None:
        """Load sessions from file."""
        try:
            if not os.path.exists(filepath):
                self.logger.warning(f"Sessions file not found: {filepath}")
                return
            
            with open(filepath, 'r') as f:
                sessions_data = json.load(f)
            
            self.sessions = []
            for session_data in sessions_data:
                # Convert timestamp strings back to datetime objects
                session_data['start_time'] = datetime.fromisoformat(session_data['start_time'])
                if session_data['end_time']:
                    session_data['end_time'] = datetime.fromisoformat(session_data['end_time'])
                
                session = UserTestSession(**session_data)
                self.sessions.append(session)
            
            self.logger.info(f"Loaded {len(self.sessions)} sessions from {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to load sessions: {e}")
    
    def export_feedback_summary(self) -> str:
        """Export a summary of all feedback for analysis."""
        if not self.sessions:
            return "No sessions available for analysis."
        
        summary = ["# User Testing Feedback Summary\n"]
        summary.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Overall statistics
        completed_sessions = [s for s in self.sessions if s.end_time]
        summary.append(f"Total Sessions: {len(completed_sessions)}\n")
        
        if completed_sessions:
            satisfaction_scores = [s.satisfaction_score for s in completed_sessions if s.satisfaction_score]
            if satisfaction_scores:
                avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores)
                summary.append(f"Average Satisfaction Score: {avg_satisfaction:.2f}/5.0\n")
            
            # Common issues
            all_issues = []
            for session in completed_sessions:
                all_issues.extend(session.issues_encountered)
            
            if all_issues:
                summary.append("\n## Common Issues\n")
                issue_frequency = {}
                for issue in all_issues:
                    issue_frequency[issue] = issue_frequency.get(issue, 0) + 1
                
                for issue, count in sorted(issue_frequency.items(), key=lambda x: x[1], reverse=True):
                    summary.append(f"- {issue} ({count} occurrences)\n")
            
            # Common suggestions
            all_suggestions = []
            for session in completed_sessions:
                all_suggestions.extend(session.suggestions)
            
            if all_suggestions:
                summary.append("\n## User Suggestions\n")
                suggestion_frequency = {}
                for suggestion in all_suggestions:
                    suggestion_frequency[suggestion] = suggestion_frequency.get(suggestion, 0) + 1
                
                for suggestion, count in sorted(suggestion_frequency.items(), key=lambda x: x[1], reverse=True):
                    summary.append(f"- {suggestion} ({count} mentions)\n")
        
        return "".join(summary)


if __name__ == "__main__":
    # Example usage
    framework = UserTestingFramework()
    
    # Create a test session
    session = framework.create_test_session("test_user_001")
    
    # Simulate some tasks
    framework.start_task(session, "device_detection")
    framework.complete_task(session, "device_detection", True, "Device detected successfully")
    
    framework.start_task(session, "template_generation")
    framework.complete_task(session, "template_generation", True, "Template created without issues")
    
    # Record some feedback
    framework.record_issue(session, "UI could be more intuitive")
    framework.record_suggestion(session, "Add keyboard shortcuts")
    framework.set_satisfaction_score(session, 4)
    
    # End session
    framework.end_session(session)
    
    # Generate reports
    session_report = framework.generate_session_report(session)
    overall_report = framework.generate_overall_report()
    
    print("Session Report:")
    print(json.dumps(session_report, indent=2))
    
    print("\nOverall Report:")
    print(json.dumps(overall_report, indent=2))
    
    # Save sessions
    framework.save_sessions("user_testing_sessions.json")