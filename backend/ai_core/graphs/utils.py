from datetime import datetime
from ..llm_api.api import get_response

def try_parse_datetime(date_str: str, allow_llm=True) -> datetime | None:
    """
    Try to parse a datetime string into a datetime object.

    Args:
        date_str (str): The datetime string to parse.
    Returns:
        datetime | None: The parsed datetime object, or None if parsing fails.
    """
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d-%m-%Y %H:%M:%S",
        "%d-%m-%Y",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    if allow_llm:
        # Try using LLM to parse the date
        prompt = f"Parse the following date string into the format YYYY-MM-DD HH:MM:SS. Respond with the timestamp ONLY: {date_str}."
        response = get_response(prompt, model="meta-llama/Llama-3.3-70B-Instruct")

        if not response:
            return None

        return try_parse_datetime(response, allow_llm=False)

    return None