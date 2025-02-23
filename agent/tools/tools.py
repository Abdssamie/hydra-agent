from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.tools.wikipedia import WikipediaToolSpec
from agent.mongo_db import query_engine


# Test function tool
def add(a: float, b: float) -> float:
    """Adds two numbers a and b"""
    return a + b


add_numbers_tool = FunctionTool.from_defaults(
    fn=add,
)

# Wikipedia Tools
wiki_tool_spec = WikipediaToolSpec()
load_data, search_data = wiki_tool_spec.to_tool_list()

# Query Engine Tool
query_tool = QueryEngineTool.from_defaults(
    query_engine, name="energy-water-nexus-data-tool",
    description="""
    This tool provides access to data from four engineering-related books/manuals:
    - Fundamentals of Wastewater Treatment and Engineering
    - Green Hydrogen Electrolysis
    - Solar Energy: A Comprehensive Guide
    - Wind Energy Explained

    Additionally, it contains two data tables:
    1. A table detailing water treatment technologies used across various industries, including treatment train
    configurations and their efficiency in removing specific contaminants.
    2. A table containing information about different chemical and biological contaminants in water.

    Use this tool only when responding to questions directly related to these topics. You may query it up to
    three times per request, refining the query each time to extract relevant data. If the tool does not provide
    a conclusive answer, offer general guidance, highlight data limitations, and suggest external resources that
    may be helpful.
    """
)

