from eden_sdk.EdenClient import EdenClient
import requests

from ai_nomic import config
from ai_nomic.util import chunk_string


def fetch_knowledge():
    eden = EdenClient(
        api_url=config.EDEN_API_URL,
        api_key=config.EDEN_API_KEY,
        api_secret=config.EDEN_API_SECRET,
    )

    character = eden.characters.get(config.EDEN_CHARACTER_ID)
    knowledge = character["character"]["logosData"]["knowledge"]
    knowledge_chunks = chunk_string(knowledge, 1980)
    return knowledge_chunks


def interrogate_knowledge(message, session_id):
    r = requests.post(
        config.EDEN_API_URL + "/characters/interact",
        json={
            "character_id": config.EDEN_CHARACTER_ID,
            "session_id": session_id,
            "message": message,
        },
        headers={
            "X-Api-Key": config.EDEN_API_KEY,
            "X-Api-Secret": config.EDEN_API_SECRET,
        },
    )
    json = r.json()
    return json["message"]
