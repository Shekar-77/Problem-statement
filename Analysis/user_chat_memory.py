from state import State
from prompt import get_user_chat_memory_messages
import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="fireworks-ai",
    api_key="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",
)

def analyze_user_chat_memory(state: State):
    print("Analyzing user chat memory results")
    user_question=state.get("user_question","")
    user_chat_memory_result=state.get("User_chat_memory_result","")

    messages=get_user_chat_memory_messages(user_question,user_chat_memory_result)

    reply=client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=messages
    )

    return {"User_chat_memory_analysis":user_chat_memory_result}