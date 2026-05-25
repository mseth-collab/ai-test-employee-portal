"""
Healthcare Clinic Bot - CLI
Run with: python -m healthcare_clinic_bot.cli
"""

from healthcare_clinic_bot.bot import handle_message, Session

def main():
    session = Session()
    print("Healthcare Clinic Bot. Type 'quit' or 'exit' to end.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "bye"):
            print("Goodbye. Take care!")
            break
        reply, session = handle_message(user_input, session)
        print(f"Bot: {reply}\n")


if __name__ == "__main__":
    main()
