from pathlib import Path
from browser_use import (
    Agent,
    AgentHistoryList,
    Browser,
    ChatGoogle,
)
import os
import dotenv

from lib.tools import extend_tools, extend_system_message
from lib.utility import create_json_file

dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


class Core:
    def __init__(
        self,
        session_name: str,
        initial_task: str = None,
        history_file: str = "agent_history.json",
        headless: bool = False,
        window_size: dict = {"width": 1280, "height": 1080},
    ):
        self.initial_task = initial_task
        self.llm = ChatGoogle(model="gemini-3-flash-preview", api_key=GOOGLE_API_KEY)
        self.history_file = Path(history_file)
        self.browser = Browser(
            headless=headless,
            window_size=window_size,
            keep_alive=True,
            record_video_dir="videos",
            user_data_dir=f"sessions/{session_name}",
            record_har_path=f"sessions/har/{session_name}.har",
            devtools=True,
        )

    async def start_agent(self):
        if not self.initial_task:
            self.initial_task = input("\n 👤 Input inital task: ")

        await self.browser.start()

        try:
            self.agent = Agent(
                browser=self.browser,
                task=self.initial_task,
                llm=self.llm,
                tools=extend_tools,
                extend_system_message=extend_system_message,
                use_judge=False,
                save_conversation_path="sessions/conversation",
            )
            history: AgentHistoryList = await self.agent.run(max_steps=2)

            while True:
                user_response = input('\n 👤 New task or "q" to quit: ')
                if str(user_response) == "q":
                    break
                self.agent.add_new_task(f"New task: {user_response}")
                await self.agent.run()
        finally:
            create_json_file("model_dump.json", history.model_dump_json())
            self.agent.save_history(self.history_file)

    async def start_replay_agent(self):
        await self.browser.start()

        self.agent = Agent(
            browser=self.browser,
            task="",
            llm=self.llm,
            tools=extend_tools,
            extend_system_message=extend_system_message,
            use_judge=False,
            save_conversation_path="conversation",
        )

        return await self.agent.load_and_rerun(
            self.history_file,
            delay_between_actions=0.1,
            max_retries=5,
            max_step_interval=1,
            ai_step_llm=None,
            summary_llm=None,
        )

    async def kill_browser(self):
        await self.browser.kill()
