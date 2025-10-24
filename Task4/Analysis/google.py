from prompt import get_google_analysis_messages
from state import State
from dotenv import load_dotenv
load_dotenv()
import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="fireworks-ai",
    api_key="",
)

def analyze_google_search(state: State):
    print("Analyzing google search results")
    user_question=state.get("user_question","")
    google_result=state.get("google_search_result","")

    messages=get_google_analysis_messages(user_question,google_result)

    reply=client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=messages
    )


    return {" google_result_analysis":reply.choices[0].message["content"]}
