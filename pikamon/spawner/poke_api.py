import requests


def get_pokemon_info(pokemon_id):
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")

    if r.status_code == 404:
        raise ValueError(r.text)
    elif r.status_code >= 400:
        raise Exception(r.text)

    return r.json()


def get_pokemon_img(pokemon_id):
    r = requests.get(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png")

    if r.status_code == 404:
        raise ValueError(r.text)
    elif r.status_code >= 400:
        raise Exception(r.text)

    return r.content


if __name__ == "__main__":
    get_pokemon_info(1)
    img = get_pokemon_img(1)
    with open("tmp.png", "wb") as f:
        f.write(img)
