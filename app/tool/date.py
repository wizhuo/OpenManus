from datetime import datetime, timedelta
from app.tool.base import BaseTool

class DateTool(BaseTool):
    """
    A tool to calculate relative dates, such as 'yesterday', '3 days ago', or custom date offsets,
    based on the current date. The days_offset is passed as a parameter to the method.
    """
    name: str = "date_tool"
    description: str = "A tool to calculate relative dates, such as 'yesterday', '3 days ago', or custom date offsets, based on current date."

    parameters: dict = {
        "type": "object",
        "properties": {
            "days_offset": {
                "type": "integer",
                "description": "Number of days to offset from the current date. E.g., -1 for yesterday, 1 for tomorrow.",
            },
            "date_format": {
                "type": "string",
                "description": "The format of the returned date, default is 'YYYY-MM-DD'.",
                "default": "%Y-%m-%d"
            },
        },
         "required": ["days_offset"],
    }

    async def execute(self, days_offset: int, date_format: str = '%Y-%m-%d') -> str:
        """
        Get a date relative to the current date. Negative values are for past dates,
        positive values are for future dates.

        Args:
            days_offset (int): The number of days to offset from the current date.
                                -1 for yesterday, 1 for tomorrow, etc.
            date_format (str): The format of the returned date, default is 'YYYY-MM-DD'.

        Returns:
            str: The relative date in the specified format.
        """
        # Always use current time as the base for calculation
        current_date = datetime.now()

        # Calculate relative date using days_offset
        relative_date = current_date + timedelta(days=days_offset)

        # Return the formatted date
        return relative_date.strftime(date_format)
