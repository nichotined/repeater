from browser_use import (
    ActionResult,
    BrowserSession,
    Tools,
)

extend_tools = Tools()
extend_system_message = (
    """
    REMEMBER you can ask human by using available tool for data input, further confirmation, validation and verification!!!
    """
)


@extend_tools.action("Ask human for help with a question")
async def ask_human(question: str, browser_session: BrowserSession) -> ActionResult:
    answer = input(f"{question} > ")
    return ActionResult(extracted_content=f"The human responded with: {answer}")
