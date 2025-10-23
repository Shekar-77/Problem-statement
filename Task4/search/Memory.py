from typing import Annotated,List
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.store.memory import InMemoryStore
from huggingface_hub import InferenceClient
import uuid

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

def embed(texts: list[str]) -> list[list[float]]:
    # This just returns deterministic vectors for demo.
    # Replace with an actual embedding model (e.g., from sentence-transformers)
    return [[float(i + 1) for i in range(10)] for _ in texts]

store = InMemoryStore(index={"embed": embed, "dims": 10})
user_id = "my-user"
application_context = "chitchat"
namespace = (user_id, application_context)

def User_chat_memory_search(state: State):
    user_input=state.get("user_question","")
    print(f"The user question{user_input}")
    store.put(
    namespace,
    f"a-memory-{uuid.uuid4()}",
    {
        "user-chat-input": [
            user_input
        ],
        "my-key": "my-value",
    },
   )
    items = store.search(namespace, filter={"my-key": "my-value"})
    user_chat_inputs=[]
    for item in items:
        value = getattr(item, "value", {})  # get the 'value' attribute safely
        if isinstance(value, dict) and "user-chat-input" in value:
            user_chat_inputs.extend(value["user-chat-input"])
    print(f"The user inputs:{user_chat_inputs}")  # flatten list
    return{"User_chat_memory_result":user_chat_inputs}
    