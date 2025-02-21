from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent
from agent.tools.tools import add_numbers_tool, load_data, search_data, query_tool
from llama_index.core.memory import ChatMemoryBuffer
from agent.llm import llm
import logging
from logging_config import setup_logging
from agent.db_store import PostgresChatStore
from config import DATABASE_URL
import sys
import io


# Ensure UTF-8 encoding for stdout and stderr
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


load_dotenv()

setup_logging()
logger = logging.getLogger(__name__)


chat_store = PostgresChatStore(DATABASE_URL)

chat_store_key = "1543-8615-7891-4961"

memory = ChatMemoryBuffer.from_defaults(
    llm=llm,
    token_limit=3000,
    chat_store=chat_store,
    # chat_store_key=chat_store_key
)

agent = ReActAgent(
    llm=llm,
    tools=[add_numbers_tool, load_data, search_data, query_tool],
    verbose=True,
    memory=memory,
    max_iterations=12,
)


def main():
    response = agent.chat("Hi again, can you search wikipedia for a concept of your choosing?")
    print(response)


if __name__ == '__main__':
    main()
