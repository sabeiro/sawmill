from fastapi import FastAPI, WebSocket, Depends, Request, HTTPException, Query
from fastapi import WebSocketException, status, Cookie
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from typing import Union

app = FastAPI()
html = open("chat.html").read()

class User(BaseModel):
  username: str
  password: str

class Settings(BaseModel):
  authjwt_secret_key: str = "secret"

@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
  return JSONResponse(status_code=exc.status_code,content={"detail": exc.message})

async def get_cookie_or_token(websocket: WebSocket,session: Union[str, None] = Cookie(default=None),
    token: Union[str, None] = Query(default=None),):
  if session is None and token is None:
    raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
  return session or token

@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(websocket: WebSocket,item_id: str,q: Union[int, None] = None,
    cookie_or_token: str = Depends(get_cookie_or_token)):
  await websocket.accept()
  while True:
    data = await websocket.receive_text()
    await websocket.send_text(
      f"Session cookie or query token value is: {cookie_or_token}"
    )
    if q is not None:
      await websocket.send_text(f"Query parameter q is: {q}")
    await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")
    
@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket('/ws')
async def websocket(websocket: WebSocket, token: str = Query(...), Authorize: AuthJWT = Depends()):
  await websocket.accept()
  while True:
    data = await websocket.receive_text()
    await websocket.send_text(f"Message text was: {data}")
  try:
    Authorize.jwt_required("websocket",token=token)
    # Authorize.jwt_optional("websocket",token=token)
    # Authorize.jwt_refresh_token_required("websocket",token=token)
    # Authorize.fresh_jwt_required("websocket",token=token)
    await websocket.send_text("Successfully Login!")
    decoded_token = Authorize.get_raw_jwt(token)
    await websocket.send_text(f"Here your decoded token: {decoded_token}")
  except AuthJWTException as err:
    await websocket.send_text(err.message)
    await websocket.close()

@app.post('/login')
def login(user: User, Authorize: AuthJWT = Depends()):
  if user.username != "test" or user.password != "test":
    raise HTTPException(status_code=401,detail="Bad username or password")

  access_token = Authorize.create_access_token(subject=user.username,fresh=True)
  refresh_token = Authorize.create_refresh_token(subject=user.username)
  return {"access_token": access_token, "refresh_token": refresh_token}

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()
