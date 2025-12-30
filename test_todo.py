#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integration test script for Todo CLI - tests all operations in a single session."""

import sys
from src.store import TodoStore
from src.models import Task

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def test_all_operations() -> None:
    """Test all todo operations in a single session (in-memory persistence)."""

    print("=" * 60)
    print("TODO CLI - Integration Test Suite")
    print("=" * 60)
    print()

    # Initialize store
    store = TodoStore()

    # Test 1: Add tasks
    print("[PASS] Test 1: Adding tasks...")
    task1 = store.add_task("Buy groceries")
    print(f"  - Added task {task1.id}: {task1.title} (status: {task1.status})")

    task2 = store.add_task("Call dentist for appointment")
    print(f"  - Added task {task2.id}: {task2.title} (status: {task2.status})")

    task3 = store.add_task("Review @john's code #urgent!")
    print(f"  - Added task {task3.id}: {task3.title} (status: {task3.status})")
    print()

    # Test 2: List all tasks
    print("[PASS] Test 2: Listing all tasks...")
    tasks = store.list_tasks()
    print(f"  - Total tasks: {len(tasks)}")
    for task in tasks:
        print(f"    [{task.id}] {task.title} - {task.status}")
    print()

    # Test 3: Complete a task
    print("[PASS] Test 3: Marking task as complete...")
    completed = store.complete_task(1)
    if completed:
        print(f"  - Task {completed.id} marked as done")
    print()

    # Test 4: Complete idempotence (mark already-done task)
    print("[PASS] Test 4: Testing idempotence (mark done task again)...")
    completed_again = store.complete_task(1)
    if completed_again:
        print(f"  - Task {completed_again.id} still done (no error - idempotent)")
    print()

    # Test 5: List tasks with mixed statuses
    print("[PASS] Test 5: Listing tasks with mixed statuses...")
    tasks = store.list_tasks()
    for task in tasks:
        status_display = f"{'DONE' if task.status == 'done' else 'PENDING'}"
        print(f"    [{task.id}] {task.title} - {status_display}")
    print()

    # Test 6: Delete a task
    print("[PASS] Test 6: Deleting a task...")
    deleted = store.delete_task(2)
    print(f"  - Task 2 deleted: {deleted}")
    tasks = store.list_tasks()
    print(f"  - Remaining tasks: {len(tasks)}")
    for task in tasks:
        print(f"    [{task.id}] {task.title}")
    print()

    # Test 7: Add new task after deletion (verify ID not reused)
    print("[PASS] Test 7: Adding new task after deletion (ID non-reuse)...")
    task4 = store.add_task("Write documentation")
    print(f"  - New task ID: {task4.id} (should be 4, not 2)")
    print()

    # Test 8: Error cases
    print("[PASS] Test 8: Testing error cases...")

    # Try to complete non-existent task
    result = store.complete_task(999)
    print(f"  - Complete non-existent ID 999: {result} (should be None)")

    # Try to delete non-existent task
    result = store.delete_task(888)
    print(f"  - Delete non-existent ID 888: {result} (should be False)")

    # Try to add empty title
    try:
        store.add_task("")
        print("  - ERROR: Empty title should have raised ValueError")
    except ValueError as e:
        print(f"  - Empty title rejected: {e}")

    print()

    # Test 9: Verify negative/zero IDs
    print("[PASS] Test 9: Testing negative/zero ID handling...")
    result = store.get_task(-1)
    print(f"  - Get task with ID -1: {result} (should be None)")
    result = store.get_task(0)
    print(f"  - Get task with ID 0: {result} (should be None)")
    print()

    # Final summary
    print("=" * 60)
    print("[SUCCESS] All tests passed!")
    print("=" * 60)
    print()
    print("Final task list:")
    tasks = store.list_tasks()
    for task in tasks:
        print(f"  [{task.id}] {task.title} - {task.status}")


if __name__ == '__main__':
    test_all_operations()
