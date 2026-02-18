import questionary
from prompt_toolkit.shortcuts import choice, yes_no_dialog
from lib.core import Core
from lib.utility import *
import asyncio
from settings import database
from prompt_toolkit.formatted_text import HTML


async def start(name: str, initial_task: str):
    history_file = "agent_history.json"
    core = Core(
        session_name=name,
        initial_task=initial_task,
        history_file=history_file,
    )
    try:
        await core.start_agent()
    finally:
        history_data = load_file_as_string(history_file)
        database.append(name, history_data)
        await core.kill_browser()


async def replay(name, history_file):
    core = Core(
        session_name=name,
        history_file=history_file,
    )
    try:
        await core.start_replay_agent()
    finally:
        history_data = load_file_as_string("agent_history_rerun.json")
        identifier = await questionary.text(
            "👤 Enter identifier of session to be stored: "
        ).ask_async()
        database.append(
            f"rerun_{name}_{identifier if identifier else 'unknown'}", history_data
        )
        await core.kill_browser()


if __name__ == "__main__":
    try:
        arg = questionary.select(
            message="👤 Select command",
            choices=[
                ("Create a new session"),
                ("Replay previous session"),
                ("Replay previous session by ID stored"),
                ("Delete stored session by ID"),
                ("Exit"),
            ],
        ).unsafe_ask()
        if arg == "Create a new session":
            name = questionary.text("👤 Enter name of session: ").unsafe_ask()
            initial_task = questionary.text(
                "👤 Enter Initial task (e.g. Open google.com): "
            ).unsafe_ask()
            asyncio.run(start(name, initial_task), debug=True)
        elif arg == "Replay previous session":
            records = database.get_all()
            if not records:
                print("No previous session found")
                exit()

            names = [data[1] for data in database.get_all()]

            name = questionary.select(
                message="👤 Select session to replay",
                choices=names,
            ).unsafe_ask()

            data = database.fetch_one_by_name(name)
            if data:
                create_json_file("agent_history_from_db.json", data[2])
                asyncio.run(
                    replay(name, "agent_history_from_db.json"),
                    debug=True,
                )
        elif arg == "Replay previous session by ID stored":
            print(database.get_all())
            id = questionary.text("👤 enter ID of session: ").unsafe_ask()
            data = database.fetch_one_by_id(id)
            create_json_file("agent_history_from_db.json", data[2])
            asyncio.run(replay(f"session_{id}", "agent_history_from_db.json"))
        elif arg == "del":
            print(database.get_all())
            id = questionary.text("👤 enter ID of session to be deleted: ").unsafe_ask()
            database.delete_by_id(id)
    except KeyboardInterrupt:
        print("Bye")
        exit()
