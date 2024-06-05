from glayout.llm.train_and_run import GlayoutLLMSessionHandler
from glayout.llm.train_and_run import run_llm_normal

session = GlayoutLLMSessionHandler()
exampleprompt = """Here is an example of strictsyntax
RegulatedCascode
create a float parameter called cascode_width
create a float parameter called feedback_width
create a float parameter called cascode_length
create a float parameter called feedback_length
create a int parameter called cascode_multiplier
create a int parameter called feedback_multiplier
create a int parameter called cascode_fingers
create a int parameter called feedback_fingers
place a nmos called cascode with width=cascode_width, length=cascode_length, fingers=cascode_fingers, rmult=1, multipliers=cascode_multiplier, with_substrate_tap=False, with_tie=False, with_dummy=False 
place a nmos called feedback with width=feedback_width, length=feedback_length, fingers=feedback_fingers, rmult=1, multipliers=feedback_multiplier, with_substrate_tap=False, with_tie=False, with_dummy=False 
move feedback below cascode
route between cascode_gate_E and feedback_drain_E using smart_route
route between feedback_gate_W and feedback_source_W using smart_route
"""
session.generate(user_input=exampleprompt)

while True:
    try:
        # Read user input
        user_input = input("Enter your input: ")
        # Pass the user input to the session handler and get the response
        response = session(user_input=user_input)
        print(response)
    except KeyboardInterrupt:
        # Gracefully exit the loop on Ctrl+C
        print("\nSession ended by user.")
        break
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")