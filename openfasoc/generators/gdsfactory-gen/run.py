import argparse
import sys
from pathlib import Path
from typing import Union
import traceback

import process_input


def reload_saved_convo(convo_file: Union[Path, str]) -> tuple:
    """restores a conversation from a .convo file

    Args:
        convo_file (Union[Path, str]): path to the .convo file

    Returns tuple:
        Session: restored conversation object
        loop_count: prompt index after restoring the conversation
    """
    savedconvo = Path(convo_file).resolve()
    if not savedconvo.is_file():
        raise FileNotFoundError("load conversation should be from an existing file")
    with savedconvo.open("r") as loadconvo:
        lines = loadconvo.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                convo = process_input.Session(inputstream=sys.stdin, outputstream=sys.stdout, toplvlname=line)
                continue
            convo.process_next_input(line)
        loop_count = len(lines) - 1
    print("\n\nloaded conversation from " + str(savedconvo))
    return convo, loop_count


def run_session(load_conversation: Union[str, Path], restore_and_exit: bool=False) -> str:
    """Manage, interact, and run conversation sessions from command line

    Returns:
        str: Glayout python code corresponding to the current session
    """
    # start convo and intialize loop counter (will be updated if we read from file)
    # if saved convo then load everything from save file, else read form stdio
    if load_conversation is not None:
        convo, loop_count = reload_saved_convo(load_conversation)
        if restore_and_exit:
            return convo.code.get_code()
    else:
        convo, loop_count = process_input.Session(inputstream=sys.stdin, outputstream=sys.stdout), int(0)
    # enter design loop
    session_ongoing = True
    while session_ongoing:
        convo.print_to_stream("\ntask " + str(loop_count))
        loop_count += 1
        convo.print_to_stream(convo.generic_prompt)
        try:
            session_ongoing = convo.process_next_input(convo.read_from_stream())
        except Exception as e:
            print(traceback.format_exc())
            print("an exception was encounterd")
            print(str(e))
            print("restoring last valid state and resuming regular program execution\n")
            convo = convo.backup
            loop_count -= 1
            session_ongoing = True
    return convo.code.get_code()


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