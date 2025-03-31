from pydantic import Field

from app.agent.toolcall import ToolCallAgent
from app.config import config
from app.prompt.browser import NEXT_STEP_PROMPT as BROWSER_NEXT_STEP_PROMPT
from app.prompt.manus import NEXT_STEP_PROMPT, SYSTEM_PROMPT
from app.tool import Terminate, ToolCollection
from app.tool.date import DateTool
from app.tool.python_execute import PythonExecute
from app.tool.str_replace_editor import StrReplaceEditor
from app.tool.shop_lookup import ShopLookup
from app.tool.sale_data import SalesData
from app.tool.member_data import MemberData
from app.util.utils import get_today

class DataAnalysisManus(ToolCallAgent):
    """
    A versatile general-purpose agent that uses planning to solve various tasks, with a focus on data retrieval and analysis.

    This agent extends BrowserAgent with a comprehensive set of tools and capabilities,
    including Python execution, web browsing, file operations, information retrieval,
    and data analysis to handle user data-related requests.
    """

    name: str = "DataAnalysisManus"
    description: str = (
        "An agent that can solve various data-related tasks using multiple tools, including data retrieval and analysis."
    )

    system_prompt: str = SYSTEM_PROMPT.format(directory=config.workspace_root)

    next_step_prompt: str =f"toda is {get_today()}:{NEXT_STEP_PROMPT}"


    max_observe: int = 10000
    max_steps: int = 20

    # Add general-purpose tools to the tool collection, including data query and analysis tools
    available_tools: ToolCollection = Field(
        default_factory=lambda: ToolCollection(
            DateTool(),
            PythonExecute(),
            Terminate(),
            ShopLookup(),
            SalesData(),
            MemberData()
        )
    )

    async def think(self) -> bool:
        """Process current state and decide next actions with appropriate context."""
        # Store original prompt
        original_prompt = self.next_step_prompt

        # Only check recent messages (last 3) for browser activity
        recent_messages = self.memory.messages[-3:] if self.memory.messages else []
        browser_in_use = any(
            "browser_use" in msg.content.lower()
            for msg in recent_messages
            if hasattr(msg, "content") and isinstance(msg.content, str)
        )

        if browser_in_use:
            # Override with browser-specific prompt temporarily to get browser context
            self.next_step_prompt = BROWSER_NEXT_STEP_PROMPT

        # Call parent's think method
        result = await super().think()

        # Restore original prompt
        self.next_step_prompt = original_prompt

        return result
