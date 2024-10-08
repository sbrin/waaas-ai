from fastapi import FastAPI
from pydantic import BaseModel
from lavague.drivers.selenium import SeleniumDriver
from lavague.core import ActionEngine, WorldModel
from lavague.core.agents import WebAgent

class TaskRequest(BaseModel):
    url: str
    task: str

def run_lavague():    
    driver = SeleniumDriver(headless=True)
    action_engine = ActionEngine(driver)
    world_model = WorldModel()
    world_model.add_knowledge(file_path="/app/knowledge1.txt")
    world_model.add_knowledge(file_path="/app/knowledge2.txt")
    return WebAgent(world_model, action_engine)

agent = run_lavague()

app = FastAPI()

@app.post("/run_task")
def run_task(request: TaskRequest):
    print(f"Received URL: {request.url}")
    print(f"Received task: {request.task}")
    
    agent.get(request.url)
    agent.run(request.task)
    return {"status": "success", "result": agent.result.output}