import requests
import json
import random


def get_pokemon_names(session: requests.Session, offset=0, limit=20) -> list:

    url = 'https://pokeapi.co/api/v2/pokemon/?offset={offset}&limit={limit}'.format(offset=offset, limit=limit)

    response = session.get(url)

    pokemon_names = []

    while response.status_code == 200:
        content = response.json()

        for pokemon in content.get('results'):
            name = pokemon.get('name')
            pokemon_names.append(name)

        next_page_url = content.get('next')
        if next_page_url is not None:
            response = session.get(next_page_url)
        else:
            break

    return pokemon_names


def get_pokemon_abilities(session: requests.Session, pokemon_name: str) -> dict:

    url = 'https://pokeapi.co/api/v2/pokemon/{name}/'.format(name=pokemon_name)
    response = session.get(url)

    abilities = {}

    if response.status_code == 200:
        content = response.json()

        for ability in content.get('abilities', []):
            ability_url = ability['ability']['url']
            ability_name = ability['ability']['name']

            effects = []

            response = session.get(ability_url)

            if response.status_code == 200:
                content = response.json()

                for effect_entry in content['effect_entries']:
                    short_effect = effect_entry['short_effect']
                    effects.append(short_effect)

            abilities[ability_name] = effects

    return abilities


def get_pokemon_info(session: requests.Session, pokemon_name: str) -> dict:

    url = 'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'.format(pokemon_name=pokemon_name)

    response = session.get(url)

    info = {}

    if response.status_code == 200:
        content = response.json()

        height = content.get('height', None)
        weight = content.get('weight', None)
        base_experience = content.get('base_experience', None)

        moves = []

        for item in content.get('moves', []):
            if 'move' in item:
                moves.append(item['move']['name'])

        types = []

        for type_ in content.get('types', []):
            types.append(type_['type']['name'])

        info['height'] = height
        info['weight'] = weight
        info['base_experience'] = base_experience
        info['moves'] = moves
        info['types'] = types

    return info


def get_location_area(session: requests.Session, pokemon_name: str) -> str:

    url = 'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/encounters'.format(pokemon_name=pokemon_name)

    response = session.get(url)

    if response.status_code == 200:
        content = response.json()

        if len(content) != 0:
            location_area = content[0]['location_area']['name']
            return location_area

    return ''


if __name__ == '__main__':
    with requests.Session() as s:
        pokemons = get_pokemon_names(s)

        count_pokemons = 10
        random_indexes = [random.randint(0, len(pokemons) - 1) for _ in range(count_pokemons)]

        print('Всего покемонов достали {}'.format(len(pokemons)))

        for idx_pokemon in random_indexes:

            pokemon = pokemons[idx_pokemon]

            print(pokemon)

            print(get_pokemon_info(s, pokemon))
            print(get_location_area(s, pokemon))
            print(get_pokemon_abilities(s, pokemon))

            print('/' * 10)

