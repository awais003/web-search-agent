import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from ddgs import DDGS

load_dotenv()

# connect to gemini using your api key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# define the we search tool that Gemini can use
def web_search(query: str) -> str:
    """Search the internet for recent information about a topic"""

    results = DDGS().text(query, max_results=5)

    # Format search results so Gemini can understand
    return "\n".join(
        f"Title: {r['title']}\nURL: {r['href']}\nSummary: {r['body']}"
        for r in results
    ) or "No search found"

# start the AI Agent
print("AI agent is ready! Type 'exist' to quite")

while True:
    question = input("You:")

    # stop the program when user type 'exit'
    if question.lower() == "exit":
        break

    try:
        # gemini decides weather to answer or use web search
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=question,
            config=types.GenerateContentConfig(
                tools=[web_search],
                system_instruction=(
                    "You are a helpful AI research assitant."
                    "Use web search when the question requires current"
                    "or additional information. Otherwise, answer directly."
                    "Base researched answers on the search results"
                )
            ),                                     
        )

        # Display final response
        print("\nAgent:", response.text, "\n")

    except Exception as e:
        print(f"\nError: {e}\n")


