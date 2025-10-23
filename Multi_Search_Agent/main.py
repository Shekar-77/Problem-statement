import langgraph
from langgraph.graph import StateGraph,START, END
from dotenv import load_dotenv
import os
from typing import Annotated,List
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from Web_search import serp_search
from search.bing import bing_search
from search.google import google_search
from search.Memory import User_chat_memory_search
from Analysis.bing import analyze_bing_search
from Analysis.google import analyze_google_search
from Analysis.user_chat_memory import analyze_user_chat_memory
from Analysis.Synthesis import synthesis_analysis

from state import State
grap_builder=StateGraph(State)

grap_builder.add_node("google_search",google_search)
grap_builder.add_node("bing_search",bing_search)
grap_builder.add_node("analyze_google_search",analyze_google_search)
grap_builder.add_node("analyze_bing_search",analyze_bing_search)
grap_builder.add_node("synthesis_analysis",synthesis_analysis)
grap_builder.add_node("user_chat_memory_search",User_chat_memory_search)
grap_builder.add_node("analyze_user_chat_memory_search",analyze_user_chat_memory)
grap_builder.add_edge(START,"google_search")
grap_builder.add_edge(START,"bing_search")
grap_builder.add_edge(START,"user_chat_memory_search")
grap_builder.add_edge("google_search","analyze_google_search")
grap_builder.add_edge("bing_search","analyze_bing_search")
grap_builder.add_edge("user_chat_memory_search","analyze_user_chat_memory_search")
grap_builder.add_edge("analyze_google_search","synthesis_analysis")
grap_builder.add_edge("analyze_bing_search","synthesis_analysis")
grap_builder.add_edge("analyze_user_chat_memory_search","synthesis_analysis")

grap_builder.add_edge("synthesis_analysis",END)

graph=grap_builder.compile()

# import streamlit as st

# prompt = st.chat_input("Say something")
# if prompt:
#     st.write(f"User has sent the following prompt: {prompt}")

def run_chatbot():

    while True:
        print("Multi-Source research Agent")
        print("Type exit to quit")
        user_input=input("Type your question")
        if user_input.lower() in "exit":
            print("Ok Bro")
            break
        state={
                "messages": [{"role":"user","content":user_input}],
                "user_question": user_input,
                "google_search_result": None,
                "bing_search_result": None,
                "User_chat_memory_result":None,
                "reddit_search_result":  None,
                "selected_reddit_urls": None,
                "reddit_post_data": None,
                "google_result_analysis": None,
                "bing_result_analysis":None,
                "reddit_search_analysis": None,
                "User_chat_memory_analysis": None,
                "final_answer": None
        }
        print("Launchin google,bing.....")
        final_state=graph.invoke(state)

        if final_state.get("final_answer"):
            print(f"The final answer:{final_state.get('final_answer')}")

if __name__=="__main__":
    run_chatbot()

# import streamlit as st  # import your LangGraph or pipeline object

# def run_chatbot():
#     st.title("🔍 Multi-Source Research Chatbot")

#     # Chat input from user
#     user_input = st.chat_input("Say something",key="User input")

#     if user_input:
#         # Exit condition
#         if user_input.lower() == "exit":
#             st.write("Ok Bro 👋")
#             st.stop()

#         # Define state
#         state = {
#             "messages": [{"role": "user", "content": user_input}],
#             "user_question": user_input,
#             "google_search_result": None,
#             "bing_search_result": None,
#             "reddit_search_result": None,
#             "selected_reddit_urls": None,
#             "reddit_post_data": None,
#             "google_result_analysis": None,
#             "bing_result_analysis": None,
#             "reddit_search_analysis": None,
#             "final_answer": None
#         }

#         st.write("🚀 Launching Google, Bing, Reddit searches...")

#         # Run your graph / workflow
#         with st.spinner("Analyzing information..."):
#             final_state = graph.invoke(state)

#         # Display final output
#         if final_state.get("final_answer"):
#             st.success(f"✅ The final answer: {final_state.get('final_answer')}")
#         else:
#             st.warning("No final answer found.")

# if __name__ == "__main__":
#     run_chatbot()



