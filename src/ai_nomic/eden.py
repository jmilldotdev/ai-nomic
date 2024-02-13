from eden_sdk.EdenClient import EdenClient
import requests

from ai_nomic import config
from ai_nomic.hedgedoc import get_doc_contents
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


def interrogate_knowledge(knowledge: str, message: str) -> str:
    # r = requests.post(
    #     config.EDEN_API_URL + "/characters/interact",
    #     json={
    #         "character_id": config.EDEN_CHARACTER_ID,
    #         "session_id": session_id,
    #         "message": message,
    #     },
    #     headers={
    #         "X-Api-Key": config.EDEN_API_KEY,
    #         "X-Api-Secret": config.EDEN_API_SECRET,
    #     },
    # )

    eden = EdenClient(
        api_url=config.EDEN_API_URL,
        api_key=config.EDEN_API_KEY,
        api_secret=config.EDEN_API_SECRET,
    )

    character = eden.characters.get(config.EDEN_CHARACTER_ID)
    name = character["character"]["name"]
    logos_data = character["character"]["logosData"]

    response = eden.characters.test(
        name=name,
        identity=logos_data["identity"],
        knowledge=knowledge,
        knowledge_summary=logos_data["knowledgeSummary"],
        message=message,
    )

    return response["message"]


def act_as_agent(name: str, identity: str) -> None:
    eden = EdenClient(
        api_url=config.EDEN_API_URL,
        api_key=config.EDEN_API_KEY,
        api_secret=config.EDEN_API_SECRET,
    )

    character = eden.characters.get(config.EDEN_CHARACTER_ID)
    logos_data = character["character"]["logosData"]

    prompt = f"""You are an agentic player playing the game of Nomic. Your stated goal is as follows:

    {identity}
    """

    response = eden.characters.test(
        name=name,
        identity=prompt,
        knowledge=logos_data["knowledge"],
        knowledge_summary=logos_data["knowledgeSummary"],
        message="It is your turn to act. Use your knowledge of the nomic rules to create a legal proposal according to your agentic goals.",
    )
    return response["message"]


def vote_as_agent(name: str, identity: str, proposal: str) -> None:
    eden = EdenClient(
        api_url=config.EDEN_API_URL,
        api_key=config.EDEN_API_KEY,
        api_secret=config.EDEN_API_SECRET,
    )

    character = eden.characters.get(config.EDEN_CHARACTER_ID)
    logos_data = character["character"]["logosData"]

    prompt = f"""You are an agentic player playing the game of Nomic. Your stated goal/identity is as follows:

    {identity}

    There is currently a proposal on the table. You must vote on it. The proposal is as follows:

    {proposal}

    Choose whether you approve or not, and provide a justification for your vote.
    """

    response = eden.characters.test(
        name=name,
        identity=prompt,
        knowledge=logos_data["knowledge"],
        knowledge_summary=logos_data["knowledgeSummary"],
        message="It is your turn to act. Use your knowledge of the nomic rules to cast a vote according to your agentic goals.",
    )
    return response["message"]
