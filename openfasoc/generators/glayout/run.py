import argparse
from glayout.syntaxer.dynamic_load import run_session
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage, interact, and run conversation sessions.")
    parser.add_argument(
        "-l",
        "--load_conversation",
        type=Path,
        help="Specify the file path to load a previous conversation",
    )
    parser.add_argument(
        "-r",
        "--restore_and_exit",
        action='store_true',
        help="Restore the conversation state and exit",
    )
    args = parser.parse_args()
    run_session(args.load_conversation, args.restore_and_exit)
