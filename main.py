from lib.core import Core
from lib.database import Database
from lib.utility import *
import asyncio

database = Database()
database.connect()
database.init_tables()


async def start(name: str, initial_task: str):
    history_file = "agent_history.json"
    core = Core(
        initial_task=initial_task,
        history_file=history_file,
    )
    await core.start_agent()

    history_data = load_file_as_string(history_file)
    database.append(name, history_data)
    await core.stop()


async def replay(history_file):
    core = Core(history_file=history_file)
    await core.start_replay_agent()
    await core.stop()


if __name__ == "__main__":
    # init db
    arg = input("\n 👤 START or RE or QUERY: ").lower()

    if arg == "start":
        name = input("\n 👤 Enter name of session: ")
        initial_task = input("\n 👤 Enter Initial task: ")
        asyncio.run(start(name, initial_task))
    elif arg == "re":
        name = input("\n 👤 enter name of session: ")
        data = database.fetch_one_by_name(name)
        create_json_file("agent_history_from_db.json", data[2])
        asyncio.run(replay("agent_history_from_db.json"))
    elif arg == "query":
        print(database.get_all())
