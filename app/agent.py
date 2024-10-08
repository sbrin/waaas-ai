# Install necessary elements
from lavague.drivers.selenium import SeleniumDriver
from lavague.core import ActionEngine, WorldModel
from lavague.core.agents import WebAgent
import json

agent = None

def run_task(url, task):
    print(f"Received URL: {url}")
    print(f"Received task: {task}")
    
    # Set URL
    agent.get(url)
    # Run agent with a specific objective
    agent.run(task)
    return agent.result.output

def application(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            post_data = environ['wsgi.input'].read(content_length)
            json_data = json.loads(post_data.decode('utf-8'))
            url = json_data.get('url')
            task = json_data.get('task')
            
            if url is None or task is None:
                start_response('400 Bad Request', [('Content-Type', 'text/plain')])
                return [b"Missing 'url' or 'task' in JSON data"]
            
            agent_result = run_task(url, task)
            
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps({'status': 'success', 'result': agent_result}).encode('utf-8')]
        except json.JSONDecodeError:
            start_response('400 Bad Request', [('Content-Type', 'text/plain')])
            return [b"Invalid JSON data"]
    else:
        start_response('405 Method Not Allowed', [('Content-Type', 'text/plain')])
        return [b"Method Not Allowed"]

def run_lavague():    
    # Set up our three key components: Driver, Action Engine, World Model
    driver = SeleniumDriver(headless=True)
    action_engine = ActionEngine(driver)
    world_model = WorldModel()
    world_model.add_knowledge(file_path="knowledge1.txt")
    world_model.add_knowledge(file_path="knowledge2.txt")
    # Create Web Agent
    return WebAgent(world_model, action_engine)

agent = run_lavague()
