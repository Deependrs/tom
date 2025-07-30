from fastapi import FastAPI
import Tom

app = FastAPI()

@app.get("/voice-command")
def voice_command(command: str):
    response = Tom.process_command(command)
    return {"response": response}
