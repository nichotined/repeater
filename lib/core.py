from pathlib import Path
from browser_use import (
    ActionResult,
    Agent,
    AgentHistoryList,
    Browser,
    ChatGoogle,
)
from browser_use.agent.views import AgentStepInfo
import os
import dotenv
import questionary

from lib.tools import extend_tools, extend_system_message
from lib.utility import *

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
        use_cache: bool = False,
    ):
        self.initial_task = initial_task
        self.history_file = Path(history_file)
        self.session_name = session_name
        self.llm = ChatGoogle(model="gemini-3-flash-preview", api_key=GOOGLE_API_KEY)
        if use_cache:
            user_data_dir = f"sessions/{session_name}"
        else:
            user_data_dir = None

        self.browser = Browser(
            headless=headless,
            window_size=window_size,
            keep_alive=True,
            record_video_dir="videos",
            user_data_dir=user_data_dir,
            record_har_path=f"sessions/har/{session_name}.har",
            devtools=True,
        )

    async def start_agent(self):
        if not self.initial_task:
            self.initial_task = questionary.text(
                "\n 👤 Input inital task: "
            ).unsafe_ask()

        await self.browser.start()

        try:
            self.agent = Agent(
                browser=self.browser,
                task=self.initial_task,
                llm=self.llm,
                tools=extend_tools,
                use_thinking=False,
                flash_mode=True,
                extend_system_message=extend_system_message,
                use_judge=False,
                save_conversation_path="sessions/conversation",
            )
            history: AgentHistoryList = await self.agent.run(max_steps=2)

            while True:
                user_response = await questionary.text(
                    '\n 👤 New task or "q" to quit (Press Option/Alt + Enter to submit): ',
                    multiline=True,
                ).ask_async()
                if str(user_response) == "q":
                    break
                self.agent.add_new_task(f"New task: {user_response}")
                await self.agent.run()
        finally:
            create_json_file("model_dump.json", history.model_dump_json())
            self.agent.save_history(self.history_file)

    async def start_replay_agent(self):
        self.agent = Agent(
            browser=self.browser,
            task="",
            llm=self.llm,
            tools=extend_tools,
            extend_system_message=extend_system_message,
            use_judge=False,
            save_conversation_path="sessions/conversation",
        )
        agent_history_list = self.agent.history.load_from_file(
            self.history_file, self.agent.AgentOutput
        )
        self.agent.history = agent_history_list

        try:
            result: list[ActionResult] = await self.agent.load_and_rerun(
                self.history_file,
                delay_between_actions=0.1,
                max_retries=2,
                max_step_interval=0.1,
                ai_step_llm=self.llm,
                summary_llm=None,
            )
            # TODO when failed, i want to ask user and continue
        except Exception as e:
            last_step_number = get_step_number(e.args[0])
            print(last_step_number)

            json_history = load_json_file("agent_history_from_db.json")
            json_steps: list = json_history.get("history")
            valid_steps = []

            for step in json_steps:
                if step["metadata"]["step_number"] < last_step_number:
                    valid_steps.append(step)
            json_steps = valid_steps
            new_history = {"history": json_steps}
            create_json_file("agent_history_valid.json", json.dumps(new_history))
            new_history_agent = self.agent.history.load_from_file(
                Path("agent_history_valid.json"), self.agent.AgentOutput
            )
            self.agent.history = new_history_agent
            print(self.agent.history.number_of_steps())
            self.agent.state.n_steps = last_step_number

            new_task = await questionary.text(
                "👤 Last step was failed. Enter new task? or 'q' to quit: ",
                multiline=True,
            ).ask_async()
            if new_task != "q":
                self.agent.add_new_task(new_task)
                await self.agent.run()
        finally:
            self.agent.save_history("agent_history_rerun.json")

    async def kill_browser(self):
        await self.browser.kill()
