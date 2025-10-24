import yfinance as yf
import pandas as pd

from huggingface_hub import InferenceClient


client = InferenceClient(
    provider="fireworks-ai",
    api_key="",
)

Symbol=input("Enter your question")

ticker_symbol = 'GOOG'
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
            f"Here is the text:{Symbol} extract the symbol of the stock market company from the text"
        )
    }
]
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
        "content": f"Here's the data — tell me if we should invest in it or not:"
    }
]


reply=client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=message_symbol
    )

print(reply.choices[0].message["content"])

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


print(reply.choices[0].message["content"])
