from fastapi import APIRouter, HTTPException, Header, UploadFile, File, Form, status, Response
from fastapi.responses import FileResponse
import logging
from api.models.chat import ChatResponse, ChatResponseWithSessionID
from agent.main import ReActAgent, memory, llm
from agent.tools.tools import query_tool, add_numbers_tool, search_data, load_data
from agent.prompts import DEFAULT_SYSTEM_PROMPT
from agent.multimodal import process_image  #, gen_img
from typing import Annotated, List
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from uuid import uuid4
from logging_config import setup_logging
from agent.clients import client
import asyncio

setup_logging()

logger = logging.getLogger(__name__)

router = APIRouter()


agent = ReActAgent(
    llm=llm,
    tools=[query_tool, add_numbers_tool, load_data, search_data],
    memory=memory,
    verbose=True,
    max_iterations=12,
)


async def ensure_system_message_stored(session_key, retries=8, delay=0.01):
    """Waits until the system message is stored, with retries."""
    for _ in range(retries):
        messages = memory.chat_store.get_messages(key=session_key)
        if any(msg.role == MessageRole.SYSTEM for msg in messages):
            return True  # System message is present, continue execution
        await asyncio.sleep(delay)  # Wait a short time before retrying
    logger.warning("System message was not found after multiple attempts")
    return False


@router.post("/chat", )
async def chat_endpoint(message: Annotated[str, Form()], file: UploadFile | None = File(None),
                        session_key: Annotated[str | None, Header()] = None):
    """Currently max of 1 file can be sent at a time."""

    send_session_key = False
    if not session_key:
        logger.info("Session-ID was not provided in headers")
        session_key = str(uuid4())
        memory.chat_store_key = session_key
        await memory.aput(
            ChatMessage(role=MessageRole.SYSTEM, content=DEFAULT_SYSTEM_PROMPT)
        )
        await ensure_system_message_stored(session_key)
        send_session_key = True
        logger.info(f"Session id generated: {session_key}")

    else:
        memory.chat_store_key = session_key
        logger.debug(f"Chat history for session key {session_key} : {memory.chat_store.get_messages(key=session_key)}")

    if file:
        # img_bytes = await file.read()
        # content_type = file.content_type
        image_prompt = process_image(client, file, message)
        message = f"User Message: {message}\n\nImage Processing Results:\n{image_prompt}"
    else:
        message = f"User Message: {message}"  # Cleaner message for no image case

    logging.debug(f"Message from request body: {message}")

    try:
        agent_response = agent.chat(message).response
        print(f"Agent response: {agent_response}")
        logging.debug(f"Agent response: {agent_response}")

        # Step 7: Return the response
        if send_session_key:
            return ChatResponseWithSessionID(message=agent_response, session_id=str(session_key))
        else:
            return ChatResponse(message=agent_response)

    except Exception as e:
        logger.exception(f"An error occurred during chat: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during chat: {e}")


@router.get("/chat_history", response_model=List[dict])
async def get_chat_history(session_key: Annotated[str | None, Header()] = None):
    try:
        chat_history = memory.chat_store.get_messages(key=session_key)
        chat_messages = [{
            "role": chat_message.role,
            "message": chat_message.content
        }
            for chat_message in chat_history]
        return chat_messages

    except Exception as e:
        logger.exception(f"An error occurred during chat: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred when retrieving chat history: {e}")


@router.delete("/del_chat_history/{session_key}", response_model=List[dict])
async def delete_chat_history(session_key: str):
    try:
        memory.chat_store.delete_messages(key=session_key)
        logging.info(f'Chat history for key: {session_key} deleted successfully')
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        logger.exception(f"An error occurred during chat history deletion: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during chat history deletion: {e}")


# @router.get("/generate_image/")
# async def generate_image(query: str):
#     file_path = await gen_img(client, query)
#     return FileResponse(file_path)
