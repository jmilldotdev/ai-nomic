from pathlib import Path
import requests
from ai_nomic import config


def new_hedgedoc():
    with open(Path(__file__).parent / "assets" / "initial_rules.md") as file:
        data = file.read()
        print(data)
    response = requests.post(
        f"{config.HEDGEDOC_API_URL}/new",
        headers={
            "Content-Type": "text/markdown",
        },
        data=data,
    )
    return response.history[0].headers["Location"]


def get_doc_contents(hedgedoc_url: str):
    response = requests.get(f"{hedgedoc_url}/download")
    response.raise_for_status()
    return response.text
