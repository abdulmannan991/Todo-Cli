#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integration test for Edit Task Title feature."""

import sys
from src.store import TodoStore

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def test_update_task_title() -> None:
    """Test update_task_title method in TodoStore."""

    print("=" * 60)
    print("EDIT TASK TITLE - Integration Test Suite")
    print("=" * 60)
    print()

    # Initialize store
    store = TodoStore()

    # Test 1: Add tasks
    print("[TEST 1] Adding test tasks...")
    task1 = store.add_task("Buy groceries")
    task2 = store.add_task("Call dentist")
    task3 = store.add_task("Write report")
    print(f"  - Added task {task1.id}: {task1.title}")
    print(f"  - Added task {task2.id}: {task2.title}")
    print(f"  - Added task {task3.id}: {task3.title}")
    print("[PASS] Test 1: Tasks added successfully")
    print()

    # Test 2: Update task title successfully
    print("[TEST 2] Updating task 1 title...")
    updated = store.update_task_title(1, "Buy groceries and milk")
    if updated and updated.title == "Buy groceries and milk":
        print(f"  - Task 1 title updated to: {updated.title}")
        print("[PASS] Test 2: Task title updated successfully")
    else:
        print("[FAIL] Test 2: Task title NOT updated")
    print()

    # Test 3: Verify the update persisted
    print("[TEST 3] Verifying update persisted...")
    task = store.get_task(1)
    if task and task.title == "Buy groceries and milk":
        print(f"  - Retrieved task 1: {task.title}")
        print("[PASS] Test 3: Update persisted correctly")
    else:
        print("[FAIL] Test 3: Update did NOT persist")
    print()

    # Test 4: Update non-existent task
    print("[TEST 4] Attempting to update non-existent task...")
    result = store.update_task_title(999, "Non-existent task")
    if result is None:
        print("  - Returned None for non-existent task ID 999")
        print("[PASS] Test 4: Non-existent task handled correctly")
    else:
        print("[FAIL] Test 4: Should return None for non-existent task")
    print()

    # Test 5: Update with empty title
    print("[TEST 5] Attempting to update with empty title...")
    try:
        store.update_task_title(2, "")
        print("[FAIL] Test 5: Should raise ValueError for empty title")
    except ValueError as e:
        print(f"  - ValueError raised: {e}")
        print("[PASS] Test 5: Empty title rejected")
    print()

    # Test 6: Update with title exceeding 1000 characters
    print("[TEST 6] Attempting to update with 1001-character title...")
    long_title = "x" * 1001
    try:
        store.update_task_title(2, long_title)
        print("[FAIL] Test 6: Should raise ValueError for title > 1000 chars")
    except ValueError as e:
        print(f"  - ValueError raised: {e}")
        print("[PASS] Test 6: Title length validation works")
    print()

    # Test 7: Update multiple tasks
    print("[TEST 7] Updating multiple tasks...")
    store.update_task_title(2, "Schedule dentist appointment")
    store.update_task_title(3, "Complete quarterly report")
    tasks = store.list_tasks()
    if (tasks[0].title == "Buy groceries and milk" and
        tasks[1].title == "Schedule dentist appointment" and
        tasks[2].title == "Complete quarterly report"):
        print("  - All tasks updated successfully:")
        for task in tasks:
            print(f"    [{task.id}] {task.title}")
        print("[PASS] Test 7: Multiple updates work correctly")
    else:
        print("[FAIL] Test 7: Multiple updates failed")
    print()

    # Test 8: Update does not affect task status
    print("[TEST 8] Verifying update doesn't affect task status...")
    store.complete_task(1)  # Mark task 1 as done
    before_status = store.get_task(1).status
    store.update_task_title(1, "Buy groceries, milk, and eggs")
    after_status = store.get_task(1).status
    if before_status == "done" and after_status == "done":
        print(f"  - Task status remained: {after_status}")
        print("[PASS] Test 8: Update doesn't affect status")
    else:
        print("[FAIL] Test 8: Update should not change status")
    print()

    # Test 9: Update does not affect task ID
    print("[TEST 9] Verifying update doesn't affect task ID...")
    original_id = task1.id
    store.update_task_title(1, "Final title for task 1")
    updated_task = store.get_task(1)
    if updated_task and updated_task.id == original_id:
        print(f"  - Task ID remained: {updated_task.id}")
        print("[PASS] Test 9: Update doesn't affect ID")
    else:
        print("[FAIL] Test 9: Update should not change ID")
    print()

    # Test 10: Special characters in title
    print("[TEST 10] Testing special characters in title...")
    result = store.update_task_title(2, "Review @john's code #urgent!")
    if result and result.title == "Review @john's code #urgent!":
        print(f"  - Special characters handled: {result.title}")
        print("[PASS] Test 10: Special characters work")
    else:
        print("[FAIL] Test 10: Special characters failed")
    print()

    # Final summary
    print("=" * 60)
    print("[SUCCESS] All edit task title tests passed!")
    print("=" * 60)
    print()
    print("Final task list:")
    tasks = store.list_tasks()
    for task in tasks:
        print(f"  [{task.id}] {task.title} - {task.status}")


def test_interactive_menu_edit() -> None:
    """Test that Edit Task option appears in interactive menu."""
    from unittest.mock import patch
    from io import StringIO
    from src.main import main

    print()
    print("=" * 60)
    print("INTERACTIVE MENU - Edit Option Test")
    print("=" * 60)
    print()

    # Simulate: Add task, Edit task, View tasks, Exit
    simulated_input = [
        "1",                                    # Choose: Add Task
        "Original title",                       # Task title
        "5",                                    # Choose: Edit Task Title
        "1",                                    # Task ID to edit
        "Updated title",                        # New title
        "2",                                    # Choose: View Tasks
        "6"                                     # Choose: Exit
    ]

    with patch('sys.argv', ['todo.py']):
        with patch('builtins.input', side_effect=simulated_input):
            old_stdout = sys.stdout
            sys.stdout = StringIO()

            try:
                exit_code = main()
                output = sys.stdout.getvalue()
                sys.stdout = old_stdout

                if "5. Edit Task Title" in output:
                    print("[PASS] Test 1: Edit Task option appears in menu")
                else:
                    print("[FAIL] Test 1: Edit Task option NOT in menu")

                if "Task 1 title updated successfully!" in output:
                    print("[PASS] Test 2: Edit success message displayed")
                else:
                    print("[FAIL] Test 2: Edit success message NOT displayed")

                if "Updated title" in output:
                    print("[PASS] Test 3: Updated title appears in task list")
                else:
                    print("[FAIL] Test 3: Updated title NOT in task list")

                if exit_code == 0:
                    print("[PASS] Test 4: Exit code is 0")
                else:
                    print(f"[FAIL] Test 4: Exit code is {exit_code}, expected 0")

                print()
                print("[SUCCESS] Interactive menu edit test completed!")

            except Exception as e:
                sys.stdout = old_stdout
                print(f"[ERROR] Test failed with exception: {e}")
                raise


if __name__ == '__main__':
    test_update_task_title()
    test_interactive_menu_edit()
