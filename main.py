# main.py
import cProfile

def main():
    """
    Entry point for the Lumi Assistant.
    Initializes the logger and starts the main conversation loop.
    """
    from utils.logger import setup_logger
    from core.controller import conversation_loop

    setup_logger()
    conversation_loop()

if __name__ == "__main__":
    cProfile.run("main()", filename="profile.out")