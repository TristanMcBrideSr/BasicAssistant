
from Config.Config import Config


class HoloAssistant:
    def __init__(self):
        self.config = Config()

    def run(self):
        while True:
            prompt = self.config.streamInput()
            if prompt.lower() in ["exit", "quit", "q"]:
                print("Exiting Holo Assistant. Goodbye!")
                break
            reply = self.config.HoloCompletion(prompt.lower())
            self.config.streamOutput(reply)


if __name__ == "__main__":
    HoloAssistant().run()
