import sys
from history_manager import load_history, save_history, clear_history
from model_manager import check_sys, unload_model, generate_response

def start_chat():
    """Interactive command-line interface chat loop."""
    print("\n" + "="*50)
    print(" === NOX AI CODING ASSISTANT (CLI MODE) ===")
    print(" Commands: /exit (quit), /clear (reset memory), /sys (hardware stats)")
    print("="*50 + "\n")

    check_sys()
    history = load_history()

    while True:
        try:
            user_input = input("\nUser: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting chat. Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == "/exit":
            print("Exiting chat. Goodbye!")
            break

        if user_input.lower() == "/clear":
            unload_model()
            clear_history()
            history = []
            print("Chat history and model memory cleared.")
            continue

        if user_input.lower() == "/sys":
            check_sys()
            continue

        try:
            print("Assistant: ", end="", flush=True)
            response = generate_response(user_input, history)
            print(response + "\n")

            history.append({"user": user_input, "assistant": response})
            save_history(history)
        except Exception as e:
            print(f"\n[CLI Error]: {e}")

if __name__ == '__main__':
    start_chat()
