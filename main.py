from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import pyautogui, threading, time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

is_typing = False
typing_thread = None

def type_text(text, delay, speed, end_key):
    global is_typing
    time.sleep(delay)
    for char in text:
        if not is_typing:
            break
        pyautogui.write(char)
        time.sleep(speed)
    if is_typing and end_key == "enter":
        pyautogui.press("enter")
    elif is_typing and end_key == "tab":
        pyautogui.press("tab")

@app.post("/start")
def start_typing(text: str = Form(...), delay: float = Form(...), speed: float = Form(...), end_key: str = Form(...)):
    global is_typing, typing_thread
    is_typing = True
    typing_thread = threading.Thread(target=type_text, args=(text, delay, speed, end_key))
    typing_thread.start()
    return {"status": "Typing started"}

@app.post("/stop")
def stop_typing():
    global is_typing
    is_typing = False
    return {"status": "Typing stopped"}
