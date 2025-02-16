from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# @router.post("/chat", )
# async def chat_endpoint(request: Request, chat_request: ChatRequest):
#     send_session_id = False
#     session_id = request.headers.get("Session-ID")
#
#     if not session_id:
#         logger.info("Session-ID was not provided in headers")
#         session_id = uuid4()
#         send_session_id = True
#         logger.info(f"Session id generated: {session_id}")
#
#     try:
#         user_input = chat_request.message
#
#         chat_history_entry = session.get(ChatHistoryModel, session_id)
#
#         chat_history = []
#         if chat_history_entry:
#             logger.info(f"Found existing session-id in database. That is: {chat_history_entry}\n")
#             loaded_chat_history = json.loads(chat_history_entry.chat_history)
#             for message in loaded_chat_history["messages"]:
#                 if message["sender"] == "user":
#                     chat_history.append(HumanMessage(content=message["message"]))
#                 elif message["sender"] == "system":
#                     chat_history.append(AIMessage(content=message["message"]))
#
#         # Step 3: Run the Langchain agent using the updated invoke_template
#         logger.debug({"input": user_input, **invoke_template})
#         agent_response = agent.invoke(
#             {"input": user_input, **invoke_template})  # Pass user input under "input" key and the rest of the context
#         agent_response_message = agent_response.get("output")
#         logger.info(str(agent_response) + f"\nType: {type(agent_response)}")
#
#         # Step 4 & 5 & 6: Prepare and save the updated chat history
#         updated_chat_history = {
#             "session_id": str(session_id),
#             "messages": [
#                 {"sender": "user", "message": user_input},
#                 {"sender": "system", "message": agent_response_message}
#             ]
#         }
#         chat_history_json = json.dumps(updated_chat_history)
#
#         if chat_history_entry:
#             chat_history_entry.chat_history = chat_history_json
#             session.commit()
#         else:
#             new_chat_history_entry = ChatHistoryModel(
#                 id=session_id,
#                 chat_history=chat_history_json,
#             )
#             session.add(new_chat_history_entry)
#             session.commit()
#         print(send_session_id)
#
#         # Step 7: Return the response
#         if send_session_id:
#             return ChatResponseV2(message=agent_response_message, session_id=str(session_id))
#         else:
#             return ChatResponse(message=agent_response_message)
#
#     except Exception as e:
#         logger.exception(f"An error occurred during chat: {e}")
#         raise HTTPException(status_code=500, detail=f"An error occurred during chat: {e}")


# @router.get("/chat_history", response_model=List[str])
# async def get_chat_history(session: SessionDep):
#     try:
#         session_id = request.headers.get("Session-ID")
#         messages = memory.chat_memory.messages
#         history = [f"{message.type}:{message.content}" for message in messages]
#         return history
#
#     except Exception as e:
#         logger.exception(f"An error occurred during chat: {e}")
#         raise HTTPException(status_code=500, detail=f"An error occurred during chat: {e}")
