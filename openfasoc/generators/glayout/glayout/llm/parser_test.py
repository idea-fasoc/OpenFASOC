import sys,os
sys.path.append('convo_parser')

from convo_parser.convoparser import Convo, ConvoParser

convo = ConvoParser("syntax_data/convos/CurrentMirrorNtype.convo").convo
print(convo.regen())