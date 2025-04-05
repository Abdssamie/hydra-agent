from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.tools.wikipedia import WikipediaToolSpec
from agent.mongo_db import query_engine


# Query Engine Tool
query_tool = QueryEngineTool.from_defaults(
    query_engine, name="energy-water-nexus-knowledge-tool",
    description="""
    This tool provides access to knowledge from four engineering-related books/manuals:
    - Fundamentals of Wastewater Treatment and Engineering
    - Green Hydrogen Electrolysis
    - Solar Energy: A Comprehensive Guide
    - Wind Energy Explained

    Additionally, it contains two knowledge tables:
    1. A table detailing water treatment technologies used across various industries, including treatment train
    configurations and their efficiency in removing specific contaminants.
    2. A table containing information about different chemical and biological contaminants in water.

    Use this tool only when responding to questions directly related to these topics. You may query it up to
    three times per request, refining the query each time to extract relevant knowledge. If the tool does not provide
    a conclusive answer, offer general guidance, highlight knowledge limitations, and suggest external resources that
    may be helpful.
    """
)

