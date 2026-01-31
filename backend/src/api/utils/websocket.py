from fastapi import FastAPI, Request, WebSocket

class WebsocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def __aenter__(self):
        self.active_connections = []  # clear all active connections
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False

    def bind_fastapi(self, app: FastAPI):
        app.state.websocket_manager = self

    @classmethod
    def from_fastapi(cls, request: Request = None, websocket: WebSocket = None):  # type: ignore
        connection = request or websocket
        return connection.app.state.websocket_manager

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception:
                self.disconnect(connection)