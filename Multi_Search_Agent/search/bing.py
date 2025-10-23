from Web_search import serp_search
from typing import Annotated,List
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
import yfinance as yf
import pandas as pd
from huggingface_hub import InferenceClient


class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_question: str| None
    google_search_result: str | None
    bing_search_result: str | None
    User_chat_memory_result: str| None
    reddit_search_result: str | None
    selected_reddit_urls: list[str] | None
    reddit_post_data: list|None
    google_result_analysis: str|None
    bing_result_analysis: str|None
    reddit_search_analysis: str | None
    User_chat_memory_analysis: str|None
    final_answer: str | None

def bing_search(state: State):
    user_question=state.get("user_question","")
    print(f"Searching bing for users question {user_question}")
    client = InferenceClient(
    provider="fireworks-ai",
    api_key="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",
    )
    start_date = '2022-01-10'
    end_date = '2025-10-10'

    message_symbol=[
        {
            "role":"system",
            "content":(
                "You are a helpful financial symbol extracter"
                "You will be given a text, from which you will have to extract the symbol of the stock market company from the text"
                "And will have to return in this format:"
                "Symbol"
            )
        },
        {
            "role":"user",
            "content":(
                f"Here is the text:{user_question} extract the symbol of the stock market company from the text"
            )
        }
    ]

    reply=client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=message_symbol
        )

    df = yf.download(reply.choices[0].message["content"], start=start_date, end=end_date)
    data=pd.DataFrame(df)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful financial analyst. "
                "You will be given historical stock data (from yfinance) in a pandas DataFrame. "
                "Based on trends, volatility, moving averages, and overall momentum, "
                "you must provide an investment recommendation: Buy, Hold, or Sell, "
                "and explain your reasoning clearly."
            )
        },
        {
            "role": "user",
            "content": f"Here's the data — tell me if we should invest in it or not:{data.to_string(index=False)}"
        }
    ]

    reply=client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=messages
        )

    return {"bing_search_result":reply.choices[0].message["content"]}