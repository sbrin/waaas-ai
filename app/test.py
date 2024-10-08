from lavague.drivers.playwright import PlaywrightDriver
from lavague.drivers.selenium import SeleniumDriver
from lavague.drivers.selenium import BrowserbaseRemoteConnection
from lavague.core import ActionEngine, WorldModel
from lavague.core.agents import WebAgent

# playwright_driver = PlaywrightDriver(headless=True)
driver = SeleniumDriver(headless=True)
action_engine = ActionEngine(driver)
world_model = WorldModel()
agent = WebAgent(world_model, action_engine)
agent.get("https://wikipedia.org")
agent.run("Search for AI")