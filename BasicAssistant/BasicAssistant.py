
import os
from dotenv import load_dotenv
from datetime import datetime
from HoloAI import HoloAI
from SkillGraph.SkillGraph import SkillGraph

# Load environment variables
load_dotenv()

# # Set These Environment Variables in your .env file or system environment variables for the provider(s) you want to use
# # PROVIDER=openai or google (default is openai)
# # OPENAI_API_KEY=your_openai_api_key
# # GOOGLE_API_KEY=your_google_api_key
# # GROQ_API_KEY=your_groq_api_key
# # ANTHROPIC_API_KEY=your_anthropic_api_key
# # XAI_API_KEY=your_xai_api_key

# #-------------------------------- NOTE --------------------------------
# # HoloAI supports OpenAI, Google, xAI, Anthropic, Groq.

# #----------------------- Provider Configuration -----------------------
PROVIDER = os.getenv("PROVIDER", "openai").lower()
# You can set it directly like this instead of using an environment variable:
# PROVIDER = "openai"  # or "google", "groq", "anthropic", "xai"

# Default user and assistant names
USER_NAME = "Tristan McBride Sr."
ASSISTANT_NAME = "Holo Assistant"

class HoloAssistant:
    def __init__(self):
        self.client     = HoloAI()
        self.skillGraph = SkillGraph()
        self.memories   = []

        # Provider configurations (default values can be overridden by env vars)
        self.providerMap = {
            "openai": {
                'response': os.getenv("OPENAI_RESPONSE_MODEL", "gpt-4.1"),
                'vision':   os.getenv("OPENAI_VISION_MODEL", "gpt-4.1")
            },
            "google": {
                'response': os.getenv("GOOGLE_RESPONSE_MODEL", "gemini-2.5-flash"),
                'vision':   os.getenv("GOOGLE_VISION_MODEL", "gemini-2.5-flash")
            },
            "groq": {
                'response': os.getenv("GROQ_RESPONSE_MODEL", "llama-3.3-70b-versatile"),
                'vision':   os.getenv("GROQ_VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")
            },
            "anthropic": {
                'response': os.getenv("ANTHROPIC_RESPONSE_MODEL", "claude-3.5-sonnet"),
                'vision':   os.getenv("ANTHROPIC_VISION_MODEL", "claude-3.5-sonnet")
            },
            "xai": {
                'response': os.getenv("XAI_RESPONSE_MODEL", "grok-4"),
                'vision':   os.getenv("XAI_VISION_MODEL", "grok-4")
            }
        }

    def currentTime(self):
        return datetime.now().strftime("%I:%M %p")

    def currentDate(self):
        return datetime.now().strftime("%B %d, %Y")

    def addMemory(self, user, response, maxTurns=10):
        self.memories.append(f"user:{user}")
        self.memories.append(f"assistant:{response}")
        if len(self.memories) > maxTurns * 2:
            self.memories = self.memories[-maxTurns*2:]

    def HoloCompletion(self, user: str) -> str:
        skills = self.skillGraph.getAgentCapabilities()
        actions = self.skillGraph.getAgentActions()

        system = f"The current user is {USER_NAME}."
        instructions = f"The current date and time is {self.currentDate()} {self.currentTime()}."

        msgs = self.client.formatConversation(self.memories, user)

        resp = self.client.HoloCompletion(
            #model=self.providerMap[PROVIDER]['response'],  # Can be used for a single model if the model can handle both response and vision
            models=[self.providerMap[PROVIDER]['response'], self.providerMap[PROVIDER]['vision']],
            system=system,
            instructions=instructions,
            input=msgs,
            skills=skills,
            actions=actions,
            tokens=4096,
            creativity=0.2
        )
        if resp:
            self.addMemory(user, resp)
        return resp

    def run(self):
        while True:
            prompt = input("You: ")
            if prompt.lower() in ["exit", "quit", "q"]:
                print("Exiting Holo Assistant. Goodbye!")
                break
            reply = self.HoloCompletion(prompt.lower())
            print(f"\n{ASSISTANT_NAME}:\n{reply}\n")


if __name__ == "__main__":
    HoloAssistant().run()
