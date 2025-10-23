from Web_search import serp_search
from typing import Annotated,List
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

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

def google_search(state: State):
    user_question=state.get("user_question","")
    print(f"Searching google for users question {user_question}")
    google_result=serp_search(user_question)
    return {"google_search_result":google_result}