"""Main entry point for the Todo CLI application.

This module integrates the CLI and storage layers with proper error handling.
All functions include strict type hints per the type-hint-enforcer skill requirement.
"""

import sys
from typing import Optional
from src.cli import create_parser, handle_add, handle_list, handle_complete, handle_delete, start_interactive_mode, Colors
from src.store import TodoStore


def main() -> int:
    """Main entry point for the Todo CLI application.

    Returns:
        Exit code (0 for success, 1 for business logic error, 2 for invalid input)
    """
    # Initialize store (in-memory, fresh each run)
    store: TodoStore = TodoStore()

    # Check if no arguments provided - start interactive mode
    if len(sys.argv) == 1:
        return start_interactive_mode(store)

    parser = create_parser()

    try:
        args = parser.parse_args()
    except SystemExit as e:
        # argparse calls sys.exit on error, catch it to handle ID validation
        exit_code: Optional[int] = e.code if isinstance(e.code, int) else 2
        if exit_code != 0:
            # argparse already printed error message
            print(f"{Colors.ERROR}Error: Invalid ID format. Please provide a positive integer.{Colors.RESET}", file=sys.stderr)
        return exit_code if exit_code is not None else 2

    # Route to appropriate handler
    if args.command == 'add':
        return handle_add(store, args)
    elif args.command == 'list':
        return handle_list(store, args)
    elif args.command == 'complete':
        return handle_complete(store, args)
    elif args.command == 'delete':
        return handle_delete(store, args)
    else:
        print(f"{Colors.ERROR}Error: Unknown command '{args.command}'{Colors.RESET}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
