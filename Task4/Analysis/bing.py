from prompt import get_bing_analysis_messages
from state import State
from dotenv import load_dotenv
load_dotenv()
import os
from huggingface_hub import InferenceClient


client = InferenceClient(
    provider="fireworks-ai",
    api_key="",
)

def analyze_bing_search(state: State):
    print("Analyzing bing search results")
    user_question=state.get("user_question","")
    bing_result=state.get("bing_search_result","")

    messages=get_bing_analysis_messages(user_question,bing_result)

    reply=client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=messages
    )

    return {"bing_result_analysis":reply.choices[0].message["content"]}
