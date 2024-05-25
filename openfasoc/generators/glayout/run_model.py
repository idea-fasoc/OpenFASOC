from glayout.llm.train_and_run import GlayoutLLMSessionHandler
from glayout.llm.train_and_run import run_llm_normal

session = GlayoutLLMSessionHandler()

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