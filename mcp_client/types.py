from typing import Literal, Union
from langchain_core.tools import BaseTool as LangchainBaseTool
from google.adk.tools.base_tool import BaseTool as AdkBaseTool

# Tool type indicator for selecting tool backend
ToolType = Literal["google", "langgraph"]

# Combined type for both langgraph and Google ADK tools
ToolUnion = Union[LangchainBaseTool, AdkBaseTool]
