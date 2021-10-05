import asyncio

from pikamon.pokeapi.api import get_pokemon
from pikamon.constants import Pokemon

loop = asyncio.get_event_loop()


def test_api_valid_pokedex_id():
    actual = loop.run_until_complete(get_pokemon(1))
    assert actual["name"] == "bulbasaur"

    actual = loop.run_until_complete(get_pokemon(4))
    assert actual["name"] == "charmander"


def test_api_invalid_pokedex_id():
    actual = loop.run_until_complete(get_pokemon(-1))
    assert actual is None

    actual = loop.run_until_complete(get_pokemon(Pokemon.MAX_ID))
    assert actual is not None

    actual = loop.run_until_complete(get_pokemon(Pokemon.MAX_ID + 1))
    assert actual is None
