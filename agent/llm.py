from llama_index.llms.gemini import Gemini
import logging
from logging_config import setup_logging


setup_logging()
logging.getLogger(__name__)

llm = Gemini(model="models/gemini-2.0-flash")
