
import requests
from pydantic import BaseModel, Field
import logging

logging.basicConfig(level=logging.DEBUG)


class Tools:
    """
    A class to provide tools for fetching and formatting biblical text via the Bible API.
    """

    ## Test changing something in the code

    class Valves(BaseModel):
        """
        A class to represent the settings for the BibleTools class.

        Attributes:
        -----------
        base_url : str
            The base URL for the Bible API.
        translation : str
            The translation version to be used for the API query.
        include_verse_numbers : bool
            A flag to include verse numbers in the API response.
        """

        base_url: str = Field(
            default="https://bible-api.com/",
            description="The base URL for the Bible API.",
        )
        translation: str = Field(
            default="web",
            description="The translation version to be used for the API query.",
        )
        include_verse_numbers: bool = Field(
            default=False,
            description="A flag to include verse numbers in the API response.",
        )

    def __init__(self):
        self.citation = (
            True  # Attribute to trigger a citation if a return occurs within the tool
        )
        self.valves = self.Valves()

    def get_bible_text(self, passage: str) -> str:
        f"""
        Fetch Bible text for a given passage or range from the Bible API and return a formatted text.
        
        
        :param passage: The Bible passage reference to query. (e.g., "Job 1:1" or "Romans 12:1-2")
        :type passage: str
        :return: Formatted text with book name, chapter, verse, and text.
        :rtype: str
        """
        try:
            params = {
                "translation": self.valves.translation,
                "include-verse-numbers": str(self.valves.include_verse_numbers).lower(),
            }
            response = requests.get(f"{self.valves.base_url}{passage}", params=params)
            response.raise_for_status()
            data = response.json()

            # Extract and format each verse in the range
            formatted_texts = []
            for verse_data in data["verses"]:
                formatted_text = (
                    f"{verse_data['book_name']} {verse_data['chapter']}:{verse_data['verse']} - "
                    f"{verse_data['text']}".strip()
                )
                formatted_texts.append(formatted_text)

            combined_text = "\n".join(formatted_texts)
            logging.debug(f"Formatted Bible texts:\n{combined_text}")
            return combined_text
        except (requests.RequestException, ValueError, IndexError, KeyError) as e:
            error_message = f"Error fetching Bible text: {str(e)}"
            logging.debug(f"Error message:\n{error_message}")
            return error_message
