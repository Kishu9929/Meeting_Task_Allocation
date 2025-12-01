"""
Test script to verify task extraction with example transcript
"""
from task_extractor import TaskExtractor
from output_formatter import OutputFormatter

example_transcript = """Hi everyone, let's discuss this week's priorities.
Sakshi, we need someone to fix the critical login bug that users reported yesterday. This needs to be done by tomorrow evening since it's blocking users.
Also, the database performance is really slow, Mohit you're good with backend optimization right? We should tackle this by end of this week, it's affecting the user experience.
And we need to update the API documentation before Friday's release - this is high priority.
Oh, and someone should design the new onboarding screens for the next sprint. Arjun, didn't you work on UI designs last month? This can wait until next Monday.
One more thing - we need to write unit tests for the payment module. This depends on the login bug fix being completed first, so let's plan this for Wednesday."""

def test_extraction():
    print("Testing task extraction with example transcript...")
    print("="*80)
    
    extractor = TaskExtractor()
    tasks = extractor.extract_tasks(example_transcript)
    
    formatter = OutputFormatter()
    formatter.display_table(tasks)
    
    print(f"\nExtracted {len(tasks)} tasks")
    return tasks

if __name__ == "__main__":
    test_extraction()

