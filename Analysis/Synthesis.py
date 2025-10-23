from prompt import get_synthesis_messages
from state import State
from dotenv import load_dotenv
load_dotenv()
import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="fireworks-ai",
    api_key="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",
)

def synthesis_analysis(state: State):
    print("Combining all results together")
    user_question=state.get("user_question","")
    google_result_analysis=state.get("google_result_analysis","")
    bing_result_analysis=state.get("bing_result_analysis","")
    user_chat_memory_analysis=state.get("User_chat_memory_analysis","")
    messages=get_synthesis_messages(user_question,google_result_analysis,bing_result_analysis,user_chat_memory_analysis)

    reply=client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=messages
    )
    final_answer=reply.choices[0].message["content"]
    return {"final_answer":final_answer, "messages":[{"role":"assistant","content":final_answer}]}