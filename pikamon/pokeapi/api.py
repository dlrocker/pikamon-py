
import aiohttp
import json
import logging

logger = logging.getLogger(__name__)

__pokemon_url = "https://pokeapi.co/api/v2/pokemon/{}"


async def get_pokemon(pokedex_id):
    """Asynchronous API call to get the information for a Pokemon by its Pokedex ID number

    Parameters
    ----------
    pokedex_id : int
        Pokedex ID number for a Pokemon. Example: Pokedex ID 1 is Bulbasaur

    Returns
    -------
    dict
        Response dictionary from the Pokemon API with the information of the specified Pokemon
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(__pokemon_url.format(pokedex_id)) as response:
            if response.status >= 400:
                return None
            response_string = await response.text()
            r = json.loads(response_string)
            return r
