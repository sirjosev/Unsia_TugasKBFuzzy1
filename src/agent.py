import os
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from src.tools import get_search_tool, assess_hoax_likelihood

# Define Agent State
class AgentState(TypedDict):
    messages: List[BaseMessage]
    news_text: str
    search_results: str
    fuzzy_assessment: dict
    final_verdict: str

# Initialize LLM
# Note: This requires OPENAI_API_KEY to be set in .env
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# --- Nodes ---

def verifier_node(state: AgentState):
    """
    Searches the internet for information related to the news text.
    """
    news_text = state["news_text"]
    search_tool = get_search_tool()
    
    print(f"--- VERIFIER: Searching for '{news_text[:50]}...' ---")
    try:
        # Search for the specific news headline or content
        results = search_tool.invoke(f"fact check {news_text}")
    except Exception as e:
        results = f"Search failed: {e}"
        
    return {"search_results": str(results)}

def analyst_node(state: AgentState):
    """
    Uses the fuzzy logic tool to assess the text style.
    """
    news_text = state["news_text"]
    print("--- ANALYST: Running Fuzzy Logic Assessment ---")
    
    assessment = assess_hoax_likelihood.invoke(news_text)
    
    return {"fuzzy_assessment": assessment}

def final_answer_node(state: AgentState):
    """
    Synthesizes search results and fuzzy assessment into a final verdict.
    """
    news_text = state["news_text"]
    search_results = state.get("search_results", "No search results.")
    fuzzy_data = state.get("fuzzy_assessment", {})
    
    print("--- FINAL ANSWER: Synthesizing ---")
    
    prompt = f"""
    You are an Expert Hoax Debunker Agent.
    
    Analyze the following news text: "{news_text}"
    
    Here is the evidence collected:
    1. **Internet Search Results**: {search_results}
    2. **Fuzzy Logic Assessment** (Text Style Analysis):
       - Caps Ratio: {fuzzy_data.get('caps_ratio_percent', 0)}%
       - Provocative Score: {fuzzy_data.get('provocative_score_raw', 0)}/100
       - Calculated Hoax Likelihood: {fuzzy_data.get('hoax_likelihood_score', 0)}%
       - Label: {fuzzy_data.get('assessment_label', 'Unknown')}
       
    Based on the external evidence (Search Results) AND the internal style analysis (Fuzzy Logic), provide a final verdict.
    
    Structure your answer as:
    - **Verdict**: [Real News / Suspicious / Hoax]
    - **Confidence**: [High/Medium/Low]
    - **Explanation**: Explain why, citing the search results and the fuzzy score.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {"final_verdict": response.content}

# --- Graph Definition ---

workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("verifier", verifier_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("final_answer", final_answer_node)

# Add Edges
# We run verifier and analyst in parallel (conceptually, or sequential here)
workflow.set_entry_point("verifier")
workflow.add_edge("verifier", "analyst")
workflow.add_edge("analyst", "final_answer")
workflow.add_edge("final_answer", END)

# Compile Graph
graph = workflow.compile()
