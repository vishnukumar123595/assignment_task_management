from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from langchain_core.messages import HumanMessage
from .agent import agent_runnable
from .api.tasks import router as tasks_router  # Fixed import
from .database import Base, engine
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount router
app.include_router(tasks_router, prefix="/api")



# ✅ Database table creation on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# ✅ WebSocket Endpoint for AI Chat
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            user_msg = await websocket.receive_text()
            print(f"Received from client: {user_msg}")
            # Send user message to the agent
            response = await agent_runnable.ainvoke({"messages": [HumanMessage(content=user_msg)]})

            # Get last message from agent response
            messages = response.get("messages", [])
            if not messages:
                await websocket.send_text("⚠️ No response from AI agent.")
                continue

            final_message = messages[-1]
            # Handle tool return (like a list of tasks) or normal message
            content = getattr(final_message, "content", "")
            if isinstance(content, str):
                await websocket.send_text(content)
            else:
                await websocket.send_text(str(content))

    except WebSocketDisconnect:
        print("Client disconnected")