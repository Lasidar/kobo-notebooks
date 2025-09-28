#!/usr/bin/env python3
"""
User Testing Demo for Kobo Notebook App

This script demonstrates the user testing framework and simulates
a complete user testing session.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.user_testing import UserTestingFramework, UserTestSession
from utils.logger import setup_logger
import json


def simulate_user_testing_session():
    """Simulate a complete user testing session."""
    logger = setup_logger("user_testing_demo")
    
    print("Kobo Notebook App - User Testing Demo")
    print("=" * 50)
    
    # Initialize testing framework
    framework = UserTestingFramework()
    
    # Simulate multiple user sessions
    users = [
        {"id": "user_001", "experience": "beginner", "device": "kobo_elipsa_2e"},
        {"id": "user_002", "experience": "intermediate", "device": "kobo_elipsa_2e"},
        {"id": "user_003", "experience": "advanced", "device": "kobo_elipsa_2e"},
        {"id": "user_004", "experience": "beginner", "device": "kobo_elipsa_2e"},
        {"id": "user_005", "experience": "intermediate", "device": "kobo_elipsa_2e"}
    ]
    
    print(f"\nSimulating {len(users)} user testing sessions...")
    
    for user in users:
        print(f"\n--- User Session: {user['id']} ({user['experience']}) ---")
        
        # Create test session
        session = framework.create_test_session(user['id'])
        
        # Simulate task completion based on user experience
        if user['experience'] == 'beginner':
            simulate_beginner_session(framework, session)
        elif user['experience'] == 'intermediate':
            simulate_intermediate_session(framework, session)
        else:  # advanced
            simulate_advanced_session(framework, session)
        
        # End session
        framework.end_session(session)
        
        print(f"Session completed for {user['id']}")
    
    # Generate reports
    print("\n" + "=" * 50)
    print("Generating User Testing Reports...")
    
    # Overall report
    overall_report = framework.generate_overall_report()
    
    # Save reports
    framework.save_sessions("user_testing_sessions.json")
    
    # Export feedback summary
    feedback_summary = framework.export_feedback_summary()
    with open("user_testing_feedback.md", 'w') as f:
        f.write(feedback_summary)
    
    # Print summary
    print(f"\nUser Testing Summary:")
    print(f"Total Sessions: {overall_report['total_sessions']}")
    print(f"Average Satisfaction Score: {overall_report['average_satisfaction_score']}/5.0")
    print(f"Total Issues: {overall_report['total_issues']}")
    print(f"Total Suggestions: {overall_report['total_suggestions']}")
    
    # Print common issues
    if overall_report['common_issues']:
        print(f"\nMost Common Issues:")
        for issue, count in overall_report['common_issues'][:5]:
            print(f"  - {issue} ({count} occurrences)")
    
    # Print common suggestions
    if overall_report['common_suggestions']:
        print(f"\nMost Common Suggestions:")
        for suggestion, count in overall_report['common_suggestions'][:5]:
            print(f"  - {suggestion} ({count} mentions)")
    
    # Print task success rates
    if overall_report['task_success_rates']:
        print(f"\nTask Success Rates:")
        for task_id, success_rate in overall_report['task_success_rates'].items():
            print(f"  - {task_id}: {success_rate:.1f}%")
    
    print(f"\nReports saved:")
    print(f"  - user_testing_sessions.json")
    print(f"  - user_testing_feedback.md")
    
    return overall_report


def simulate_beginner_session(framework, session):
    """Simulate a beginner user session."""
    # Beginner users typically complete basic tasks with some difficulties
    
    # Device detection - usually successful
    framework.start_task(session, "device_detection")
    framework.complete_task(session, "device_detection", True, "Device detected successfully")
    
    # Template generation - might have some issues
    framework.start_task(session, "template_generation")
    success = True  # Assume success for demo
    notes = "Generated lined template with default settings"
    framework.complete_task(session, "template_generation", success, notes)
    
    # Template preview - usually successful
    if success:
        framework.start_task(session, "template_preview")
        framework.complete_task(session, "template_preview", True, "Preview worked well")
    
    # Package creation - might struggle
    framework.start_task(session, "package_creation")
    success = True  # Assume success for demo
    notes = "Created package after some trial and error"
    framework.complete_task(session, "package_creation", success, notes)
    
    # Device backup - might be confused
    framework.start_task(session, "device_backup")
    success = True  # Assume success for demo
    notes = "Backup created successfully with help from documentation"
    framework.complete_task(session, "device_backup", success, notes)
    
    # Template installation - might be hesitant
    if success:
        framework.start_task(session, "template_installation")
        success = True  # Assume success for demo
        notes = "Installation completed successfully"
        framework.complete_task(session, "template_installation", success, notes)
    
    # Record feedback
    framework.record_issue(session, "UI could be more intuitive for beginners")
    framework.record_issue(session, "Need more help text and tooltips")
    framework.record_suggestion(session, "Add a beginner mode with guided setup")
    framework.record_suggestion(session, "Include more examples and tutorials")
    
    framework.add_feedback(session, "experience", {
        "difficulty": "moderate",
        "time_taken": "longer than expected",
        "help_needed": True,
        "would_recommend": True
    })
    
    framework.set_satisfaction_score(session, 3)  # Moderate satisfaction


def simulate_intermediate_session(framework, session):
    """Simulate an intermediate user session."""
    # Intermediate users typically complete most tasks successfully
    
    # Device detection - successful
    framework.start_task(session, "device_detection")
    framework.complete_task(session, "device_detection", True, "Device detected quickly")
    
    # Template generation - successful
    framework.start_task(session, "template_generation")
    framework.complete_task(session, "template_generation", True, "Generated multiple template types")
    
    # Template preview - successful
    framework.start_task(session, "template_preview")
    framework.complete_task(session, "template_preview", True, "Preview functionality works well")
    
    # Package creation - successful
    framework.start_task(session, "package_creation")
    framework.complete_task(session, "package_creation", True, "Package creation straightforward")
    
    # Device backup - successful
    framework.start_task(session, "device_backup")
    framework.complete_task(session, "device_backup", True, "Backup process clear and easy")
    
    # Template installation - successful
    framework.start_task(session, "template_installation")
    framework.complete_task(session, "template_installation", True, "Installation completed without issues")
    
    # Template library - successful
    framework.start_task(session, "template_library")
    framework.complete_task(session, "template_library", True, "Library management intuitive")
    
    # Advanced features - might try but not complete
    framework.start_task(session, "advanced_features")
    success = True  # Assume success for demo
    notes = "Tried batch operations, worked well"
    framework.complete_task(session, "advanced_features", success, notes)
    
    # Record feedback
    framework.record_issue(session, "Some advanced features could be better documented")
    framework.record_suggestion(session, "Add keyboard shortcuts for power users")
    framework.record_suggestion(session, "Include template sharing functionality")
    
    framework.add_feedback(session, "experience", {
        "difficulty": "easy",
        "time_taken": "as expected",
        "help_needed": False,
        "would_recommend": True
    })
    
    framework.set_satisfaction_score(session, 4)  # Good satisfaction


def simulate_advanced_session(framework, session):
    """Simulate an advanced user session."""
    # Advanced users typically complete all tasks successfully and quickly
    
    # Complete all basic tasks quickly
    tasks = [
        "device_detection",
        "template_generation", 
        "template_preview",
        "package_creation",
        "device_backup",
        "template_installation",
        "template_library",
        "advanced_features"
    ]
    
    for task in tasks:
        framework.start_task(session, task)
        framework.complete_task(session, task, True, f"Completed {task} successfully")
    
    # Record feedback
    framework.record_issue(session, "Would like more customization options")
    framework.record_suggestion(session, "Add plugin system for custom template generators")
    framework.record_suggestion(session, "Include command-line interface")
    framework.record_suggestion(session, "Add automation and scripting capabilities")
    
    framework.add_feedback(session, "experience", {
        "difficulty": "very easy",
        "time_taken": "faster than expected",
        "help_needed": False,
        "would_recommend": True,
        "power_user_features": "would be appreciated"
    })
    
    framework.set_satisfaction_score(session, 5)  # High satisfaction


def analyze_user_testing_results():
    """Analyze user testing results and provide insights."""
    print("\n" + "=" * 50)
    print("User Testing Analysis")
    print("=" * 50)
    
    # Load session data
    try:
        with open("user_testing_sessions.json", 'r') as f:
            sessions_data = json.load(f)
        
        print(f"Loaded {len(sessions_data)} user sessions")
        
        # Analyze by user experience
        experience_stats = {}
        for session_data in sessions_data:
            user_id = session_data['user_id']
            experience = "beginner" if "001" in user_id or "004" in user_id else \
                        "intermediate" if "002" in user_id or "005" in user_id else "advanced"
            
            if experience not in experience_stats:
                experience_stats[experience] = {
                    "sessions": 0,
                    "satisfaction_scores": [],
                    "issues": [],
                    "suggestions": []
                }
            
            experience_stats[experience]["sessions"] += 1
            if session_data.get('satisfaction_score'):
                experience_stats[experience]["satisfaction_scores"].append(session_data['satisfaction_score'])
            
            experience_stats[experience]["issues"].extend(session_data.get('issues_encountered', []))
            experience_stats[experience]["suggestions"].extend(session_data.get('suggestions', []))
        
        # Print analysis by experience level
        for experience, stats in experience_stats.items():
            print(f"\n{experience.title()} Users:")
            print(f"  Sessions: {stats['sessions']}")
            if stats['satisfaction_scores']:
                avg_satisfaction = sum(stats['satisfaction_scores']) / len(stats['satisfaction_scores'])
                print(f"  Average Satisfaction: {avg_satisfaction:.1f}/5.0")
            print(f"  Issues: {len(stats['issues'])}")
            print(f"  Suggestions: {len(stats['suggestions'])}")
        
        # Identify patterns
        print(f"\nKey Insights:")
        print(f"  - Beginner users need more guidance and help")
        print(f"  - Intermediate users find the application intuitive")
        print(f"  - Advanced users want more power-user features")
        print(f"  - Overall satisfaction is good across all user types")
        print(f"  - Main areas for improvement: UI intuitiveness and documentation")
        
    except FileNotFoundError:
        print("No user testing sessions found. Run the simulation first.")


if __name__ == "__main__":
    # Run the user testing simulation
    report = simulate_user_testing_session()
    
    # Analyze the results
    analyze_user_testing_results()
    
    print(f"\nUser Testing Demo completed successfully!")
    print(f"Check the generated files for detailed results.")