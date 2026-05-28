from browser_use import Agent, Browser, ChatBrowserUse
import asyncio


class BrowerUser:
    def __init__(self) -> None:
        self.browser = Browser()

    async def main(self):
        # 1. 启动浏览器

        # 2. 创建一个 Agent，告诉它任务目标
        agent = Agent(
            task="Find the number of stars of the browser-use repo",  # 任务：找到 browser-use 仓库的 star 数量
            llm=ChatBrowserUse(),  # 使用官方优化过的 LLM
            browser=self.browser,
        )

        # 3. 运行 Agent，看它表演
        await agent.run()

    def start(self):
        asyncio.run(self.main())
