from lavague.drivers.playwright import PlaywrightDriver
from lavague.drivers.selenium import SeleniumDriver
from lavague.core import ActionEngine, WorldModel
from lavague.core.agents import WebAgent
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

global agent

def run_task(
        url, task):
    print(f"Received URL: {url}")
    print(f"Received task: {task}")
    
    # Set URL
    agent.get(url)
    # Run agent with a specific objective
    agent.run(task)
    return agent.result.output

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            json_data = json.loads(post_data.decode('utf-8'))
            url = json_data.get('url')
            task = json_data.get('task')
            
            if url is None or task is None:
                self.send_error(400, "Missing 'url' or 'task' in JSON data")
                return
            
            agent_result = run_task(url, task)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success', 'result': agent_result}).encode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON data")

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

def run_lavague():    
    # Set up our three key components: Driver, Action Engine, World Model
    driver = PlaywrightDriver(headless=True)
    action_engine = ActionEngine(driver)
    world_model = WorldModel()
    world_model.add_knowledge(file_path="knowledge1.txt")
    world_model.add_knowledge(file_path="knowledge2.txt")
    # Create Web Agent
    return WebAgent(world_model, action_engine)

if __name__ == "__main__":
    agent = run_lavague()
    run_server()
