from browser_use import Agent, Browser
from .browser_use_llm import BrowserUseLlm
import asyncio


class BrowerUser:
    def __init__(self) -> None:
        self.browser = Browser()

    async def main(self):
        agent = Agent(
            task="Find the number of stars of the browser-use repo",
            llm=BrowserUseLlm("codeagent"),
            browser=self.browser,
        )
        await agent.run()

    def start(self):
        asyncio.run(self.main())