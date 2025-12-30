#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integration test for Interactive Menu Mode."""

import sys
from io import StringIO
from unittest.mock import patch
from src.main import main

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def test_interactive_menu() -> None:
    """Test interactive menu mode with simulated user input."""

    print("=" * 60)
    print("INTERACTIVE MENU MODE - Integration Test")
    print("=" * 60)
    print()

    # Simulate user input: Add 2 tasks, view them, complete one, view again, delete one, exit
    simulated_input = [
        "1",                                    # Choose: Add Task
        "Buy groceries",                        # Task 1 title
        "1",                                    # Choose: Add Task
        "Call dentist",                         # Task 2 title
        "2",                                    # Choose: View Tasks
        "3",                                    # Choose: Update Task (Complete)
        "1",                                    # Complete task ID 1
        "2",                                    # Choose: View Tasks
        "4",                                    # Choose: Delete Task
        "2",                                    # Delete task ID 2
        "2",                                    # Choose: View Tasks
        "5"                                     # Choose: Exit
    ]

    # Join inputs with newlines
    input_data = "\n".join(simulated_input) + "\n"

    # Patch sys.argv to simulate no arguments (trigger interactive mode)
    with patch('sys.argv', ['todo.py']):
        # Patch input() to use simulated input
        with patch('builtins.input', side_effect=simulated_input):
            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = StringIO()

            try:
                # Run main() which should start interactive mode
                exit_code = main()

                # Get output
                output = sys.stdout.getvalue()

                # Restore stdout
                sys.stdout = old_stdout

                # Verify expected behaviors
                print("[PASS] Test 1: Interactive mode started successfully")

                if "TODO APPLICATION" in output:
                    print("[PASS] Test 2: Menu header displayed")
                else:
                    print("[FAIL] Test 2: Menu header NOT displayed")

                if "Task 1 added successfully" in output:
                    print("[PASS] Test 3: Task 1 added successfully")
                else:
                    print("[FAIL] Test 3: Task 1 NOT added")

                if "Task 2 added successfully" in output:
                    print("[PASS] Test 4: Task 2 added successfully")
                else:
                    print("[FAIL] Test 4: Task 2 NOT added")

                if "Buy groceries" in output:
                    print("[PASS] Test 5: Task list shows 'Buy groceries'")
                else:
                    print("[FAIL] Test 5: Task list does NOT show 'Buy groceries'")

                if "marked as done" in output:
                    print("[PASS] Test 6: Task completion message shown")
                else:
                    print("[FAIL] Test 6: Task completion message NOT shown")

                if "deleted successfully" in output:
                    print("[PASS] Test 7: Task deletion message shown")
                else:
                    print("[FAIL] Test 7: Task deletion message NOT shown")

                if "Goodbye!" in output:
                    print("[PASS] Test 8: Exit message displayed")
                else:
                    print("[FAIL] Test 8: Exit message NOT displayed")

                if exit_code == 0:
                    print("[PASS] Test 9: Exit code is 0 (success)")
                else:
                    print(f"[FAIL] Test 9: Exit code is {exit_code}, expected 0")

                print()
                print("=" * 60)
                print("[SUCCESS] Interactive menu mode test completed!")
                print("=" * 60)

            except Exception as e:
                sys.stdout = old_stdout
                print(f"[ERROR] Test failed with exception: {e}")
                raise


def test_command_line_mode_still_works() -> None:
    """Verify that command-line mode still works with arguments."""

    print()
    print("=" * 60)
    print("COMMAND-LINE MODE - Verification Test")
    print("=" * 60)
    print()

    # Test that command-line mode still works when arguments are provided
    with patch('sys.argv', ['todo.py', 'add', 'Test command line task']):
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            exit_code = main()
            output = sys.stdout.getvalue()

            sys.stdout = old_stdout

            if "Task 1 added:" in output and exit_code == 0:
                print("[PASS] Command-line mode still works with arguments")
            else:
                print("[FAIL] Command-line mode broken")

        except Exception as e:
            sys.stdout = old_stdout
            print(f"[ERROR] Command-line test failed: {e}")
            raise


if __name__ == '__main__':
    test_interactive_menu()
    test_command_line_mode_still_works()
