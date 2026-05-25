"""CLI: python -m bestfraiend.cli"""
from bestfraiend.bot import Session, handle_message


def main():
    session = Session()
    print("BestFrAIend — type 'quit' to exit.\n")
    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not text:
            continue
        if text.lower() in ("quit", "exit", "bye"):
            print("BestFrAIend: Goodbye! I'm here whenever you need policy answers.\n")
            break
        reply, session = handle_message(text, session)
        print(f"BestFrAIend: {reply}\n")


if __name__ == "__main__":
    main()
