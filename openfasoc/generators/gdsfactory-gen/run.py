import argparse
from pathlib import Path
import sys
from process_input import Session

# parse args
parser = argparse.ArgumentParser(description="Load conversation from a file")
parser.add_argument("-l","--load_conversation", type=Path, help="Specify the file path to load a previous conversation")
args = parser.parse_args()
# intialize loop counter (will be updated if we read from file)
loop_count = int(0)
# start convo
# if saved convo then load everything from save file, else read form stdin
if args.load_conversation is not None:
	savedconvo = Path(args.load_conversation).resolve()
	if not savedconvo.is_file():
		raise FileNotFoundError("load conversation should be from an existing file")
	with savedconvo.open("r") as loadconvo:
		lines = loadconvo.readlines()
		for i, line in enumerate(lines):
			if i==0:
				convo = Session(inputstream=sys.stdin,outputstream=sys.stdout,toplvlname=line)
				continue
			convo.process_next_input(line)
		loop_count=len(lines)-1
	print("\n\nloaded conversation from "+str(savedconvo))
	print("You can now continue providing inputs")
else:
	convo = Session(inputstream=sys.stdin,outputstream=sys.stdout)
# enter design loop
session_ongoing = True
while(session_ongoing):
	convo.print_to_stream("\ntask "+str(loop_count))
	loop_count += 1
	convo.print_to_stream(convo.generic_prompt)
	try:
		session_ongoing = convo.process_next_input(convo.read_from_stream())
	except Exception as e:
		print("an exception was encounterd")
		print(str(e))
		print("restoring last valid state and resuming regular program execution\n")
		convo = convo.backup
		loop_count -= 1
		session_ongoing = True
