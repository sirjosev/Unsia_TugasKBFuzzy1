import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool

# Initialize Search Tool
# We prefer Tavily if available, else DuckDuckGo
def get_search_tool():
    if os.environ.get("TAVILY_API_KEY"):
        return TavilySearchResults(max_results=3)
    else:
        wrapper = DuckDuckGoSearchAPIWrapper(max_results=3)
        return DuckDuckGoSearchResults(api_wrapper=wrapper)

# Tool wrapper for the existing Fuzzy Logic
from src.fuzzy_logic import FuzzySystem
from src.nlp_engine import NLPEngine

nlp = NLPEngine()
fuzzy = FuzzySystem()

@tool
def assess_hoax_likelihood(text: str):
    """
    Analyzes the text using fuzzy logic based on caps ratio and provocative words.
    Returns a hoax likelihood score (0-100) and a classification label.
    Use this tool to get a quantitative assessment of the text style.
    """
    analysis = nlp.analyze(text)
    caps = analysis['caps_ratio']
    prov = analysis['provocative_score']
    
    score, label = fuzzy.calculate(caps, prov)
    
    return {
        "caps_ratio_percent": caps,
        "provocative_score_raw": prov,
        "hoax_likelihood_score": score,
        "assessment_label": label
    }
