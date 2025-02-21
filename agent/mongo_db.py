from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core import VectorStoreIndex
import pymongo
from config import MONGODB_URL
from agent.llm import llm
import logging
from logging_config import setup_logging
import ssl

setup_logging()
logging.getLogger(__name__)


def get_mongo_client(mongo_uri):
    """Establish connection to the MongoDB."""
    try:
        client = pymongo.MongoClient(mongo_uri, tlsInsecure=True)
        logging.info("Connection to MongoDB successful")
        return client
    except pymongo.errors.ConfigurationError as e:
        logging.error(f"Connection failed: {e}")
        return None
    except pymongo.errors.ServerSelectionTimeputError as e:
        logging.error(f"Connection Timeout Error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None


mongo_uri = MONGODB_URL
mongo_client = get_mongo_client(mongo_uri)
COLLECTION_NAME = "hydra_agent_collection"
db = mongo_client["default_db"]

collection = db[COLLECTION_NAME]

logging.debug("Initializing vector store from MongoDBAtlas")
# Initialize the vector store
vector_store = MongoDBAtlasVectorSearch(
    mongo_client,
    collection_name=COLLECTION_NAME,
    vector_index_name="vector_index"
)
logging.debug("Finished initializing vector store from MongoDBAtlas")

logging.debug("Creating an index from MongoDB vector store")
index = VectorStoreIndex.from_vector_store(vector_store)
logging.debug("Done creating an index")

logging.debug("Using index as a query engine")
query_engine = index.as_query_engine(llm=llm)
