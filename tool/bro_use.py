from browser_use import Agent
import asyncio
import os

os.environ.setdefault("BROWSER_USE_API_KEY", "")


async def main():
    agent = Agent(
        task="""登录流程演示：
        1. 打开 https://ui.appen.com.cn/user/login
        2. 在用户名输入框输入 'testuser'
        3. 在密码输入框输入 'password123'
        4. 点击登录按钮
        5. 等待页面跳转完成
        """,
    )

    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
