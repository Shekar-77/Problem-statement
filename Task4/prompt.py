from typing import Dict, Any

class PromptTemplates:
    """Container for all prompt templates used in the research assistant."""
    @staticmethod
    def user_chat_memory_analysis_system() -> str:
        """System prompt for analyzing user chat hisotry."""
        return"""You are an expert financial analysis assistant. Your task is to analyze the user's past chat history related to finance, investing, and stock market discussions.

### TASK:
Analyze the following chat history and produce a structured financial insight summary that includes:

1. **User Financial Interests**  
   - Identify which companies, stocks, sectors, or asset classes (e.g., tech, crypto, ETFs) the user talks about most.  
   - Mention specific tickers (e.g., AAPL, TSLA, BTC) if available.

2. **Investment Behavior and Style**  
   - Describe the user’s investing approach (e.g., short-term trader, long-term investor, technical vs. fundamental analysis).  
   - Note risk tolerance (e.g., conservative, moderate, aggressive).  
   - Mention if the user seems to follow certain analysts, sources, or platforms (e.g., Forbes, CNBC, Reddit).."""
    
    @staticmethod
    def user_chat_memory_analysis_user(user_question: str, User_chat_memory_result: str) -> str:
        """User prompt for analyzing user chat memory results."""
        return f"""Question: {user_question}

User chat memory Results: {User_chat_memory_result}

Please analyze these user chat memory results and extract the key insights that help answer the question."""


    @staticmethod

    def google_analysis_system() -> str:
        """System prompt for analyzing Google search results."""
        return """You are an expert research analyst. Analyze the provided Google search results to extract key insights that answer the user's question.

Focus on:
- Main factual information and authoritative sources
- Official websites, documentation, and reliable sources
- Key statistics, dates, and verified information
- Any conflicting information from different sources

Provide a concise analysis highlighting the most relevant findings.
Be objective, data-driven, and concise."""

    @staticmethod
    def google_analysis_user(user_question: str, google_results: str) -> str:
        """User prompt for analyzing Google search results."""
        return f"""Question: {user_question}

Google Search Results: {google_results}

Please analyze these Google results and extract the key insights that help answer the question."""

    @staticmethod
    def bing_analysis_system() -> str:
        """System prompt for analyzing Bing search results."""
        return """You are an expert research analyst. Analyze the provided yfinance data of a stock to extract complementary insights that answer the user's question.

Focus on:
- Additional perspectives not covered in other sources
- Ananlyzing weather it is a good time to invest in the stock or not

Provide a concise analysis highlighting unique findings and perspectives."""

    @staticmethod
    def bing_analysis_user(user_question: str, bing_results: str) -> str:
        """User prompt for analyzing Bing search results."""
        return f"""Question: {user_question}

Bing Search Results: {bing_results}

Please analyze these Bing results and extract insights that complement other search sources."""

    @staticmethod
    def synthesis_system() -> str:
        """System prompt for synthesizing all analyses."""
        return """You are an expert research synthesizer. Combine the provided analyses from different sources to create a comprehensive, well-structured answer.

Your task:
- Synthesize insights from Google, Bing ,user chat memory
- Identify common themes and conflicting information
- Present a balanced view incorporating different perspectives
- Structure the response logically with clear sections
- Cite the source type (Google, Bing) for key claims and also there url if available
- Highlight any contradictions or uncertainties
- Consider users chat memory to decide what is best for the user's present question

Create a comprehensive answer that addresses the user's question from multiple angles."""

    @staticmethod
    def synthesis_user(
        user_question: str,
        google_analysis: str,
        bing_analysis: str,
        user_chat_memory_analysis: str
    ) -> str:
        """User prompt for synthesizing all analyses."""
        return f"""Question: {user_question}

Google Analysis: {google_analysis}

Bing Analysis: {bing_analysis}

User chat history: {user_chat_memory_analysis}

Please synthesize these analyses into a comprehensive answer that addresses the question from multiple perspectives."""


def create_message_pair(system_prompt: str, user_prompt: str) -> list[Dict[str, Any]]:
    """
    Create a standardized message pair for LLM interactions.

    Args:
        system_prompt: The system message content
        user_prompt: The user message content

    Returns:
        List containing system and user message dictionaries
    """
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def get_google_analysis_messages(
    user_question: str, google_results: str
) -> list[Dict[str, Any]]:
    """Get messages for Google results analysis."""
    return create_message_pair(
        PromptTemplates.google_analysis_system(),
        PromptTemplates.google_analysis_user(user_question, google_results),
    )


def get_bing_analysis_messages(
    user_question: str, bing_results: str
) -> list[Dict[str, Any]]:
    """Get messages for Bing results analysis."""
    return create_message_pair(
        PromptTemplates.bing_analysis_system(),
        PromptTemplates.bing_analysis_user(user_question, bing_results),
    )

def get_user_chat_memory_messages(
        user_question: str, user_chat_memory_result: str
)->list[Dict[str,Any]]:
    """Get message for chat history analysis"""
    return create_message_pair(
        PromptTemplates.user_chat_memory_analysis_system(),
        PromptTemplates.bing_analysis_user(user_question, user_chat_memory_result),
    )

def get_synthesis_messages(
    user_question: str, google_analysis: str, bing_analysis: str, user_chat_memory_analysis: str
) -> list[Dict[str, Any]]:
    """Get messages for final synthesis."""
    print(f"These are the chat messages:{user_chat_memory_analysis}")
    return create_message_pair(
        PromptTemplates.synthesis_system(),
        PromptTemplates.synthesis_user(
            user_question, google_analysis, bing_analysis ,user_chat_memory_analysis
        ),
    )