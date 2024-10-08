from fastapi import FastAPI
from lavague.drivers.selenium import SeleniumDriver
from lavague.core import ActionEngine, WorldModel
from lavague.core.agents import WebAgent

def run_lavague():    
    driver = SeleniumDriver(headless=True)
    action_engine = ActionEngine(driver)
    world_model = WorldModel()
    world_model.add_knowledge(file_path="knowledge1.txt")
    world_model.add_knowledge(file_path="knowledge2.txt")
    return WebAgent(world_model, action_engine)

agent = run_lavague()

app = FastAPI()

# @app.get("/")
# def read_root():
#     agent.get("https://wikipedia.org")
#     agent.run("Search for AI and return it's definition")
#     return {"result": agent.result.output}

@app.post("/run_task")
async def run_task(request):
    if not request.url or not request.task:
        return {"status": "error", "message": "URL and task must be defined"}
    
    print(f"Received URL: {request.url}")
    print(f"Received task: {request.task}")
    
    agent.get(request.url)
    agent.run(request.task)
    return {"status": "success", "result": agent.result.output}