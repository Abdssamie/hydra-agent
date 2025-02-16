from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent
from llama_index.llms.gemini import Gemini
from llama_index.core.memory import ChatMemoryBuffer
# from llama_index.core.base.llms.types import ChatMessage, MessageRole
# from prompts import DEFAULT_SYSTEM_PROMPT
from llama_index.core.tools import FunctionTool  # , ToolMetadata
import logging
from db_store import PostgresChatStore
from config import DATABASE_URL
# import asyncio


load_dotenv()

logger = logging.getLogger(__name__)


def add(a: float, b: float) -> float:
    """Adds two numbers a and b"""
    return a + b


add_numbers_tool = FunctionTool.from_defaults(
    fn=add,
)

llm = Gemini(model="models/gemini-2.0-flash")

chat_store = PostgresChatStore(DATABASE_URL)

chat_store_key = "1543-8615-7891-4961"

memory = ChatMemoryBuffer.from_defaults(
    llm=llm,
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key=chat_store_key
)

# memory.reset()
# memory.put(
#     ChatMessage(role=MessageRole.SYSTEM, content=DEFAULT_SYSTEM_PROMPT)
# )


agent = ReActAgent(
    llm=llm,
    tools=[add_numbers_tool],
    verbose=True,
    memory=memory,
    max_iterations=12,
)


def main():
    response = agent.chat("VERY NICE! Can you name the operations you just did in the last two messages?")
    print(response)


if __name__ == '__main__':
    main()
