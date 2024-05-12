import aiohttp
import asyncio
import random

async def fetch_pokemon_data(session, name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    async with session.get(url) as response:
        data = await response.json()
        return data

async def get_pokemon_stats(session, pokemon_name):
    data = await fetch_pokemon_data(session, pokemon_name)
    stats = {
        'attack': data['stats'][4]['base_stat'],
        'defense': data['stats'][3]['base_stat'],
        'speed': data['stats'][0]['base_stat']
    }
    return stats

async def main():
    pokemon_names = ['charmander', 'squirtle', 'bulbasaur', 'pikachu', 'eevee', 'jigglypuff', 'snorlax', 'magikarp', 'mewtwo', 'dragonite']

    async with aiohttp.ClientSession() as session:
        tasks = [get_pokemon_stats(session, name) for name in pokemon_names]
        pokemon_stats = await asyncio.gather(*tasks)

    return dict(zip(pokemon_names, pokemon_stats))

def simulate_battle(pokemon_stats):
    pokemon1, pokemon2 = random.sample(list(pokemon_stats.keys()), 2)
    pokemon1_stats = pokemon_stats[pokemon1]
    pokemon2_stats = pokemon_stats[pokemon2]

    pokemon1_strength = sum(pokemon1_stats.values())
    pokemon2_strength = sum(pokemon2_stats.values())

    if pokemon1_strength > pokemon2_strength:
        winner = pokemon1
    elif pokemon2_strength > pokemon1_strength:
        winner = pokemon2
    else:
        winner = "It's a tie!"

    battle_result = {
        'pokemon1': {'name': pokemon1, 'stats': pokemon1_stats},
        'pokemon2': {'name': pokemon2, 'stats': pokemon2_stats},
        'winner': winner
    }

    return battle_result

if __name__ == "__main__":
    pokemon_stats = asyncio.run(main())

    battle_result = simulate_battle(pokemon_stats)
    print("Battle Result:")
    print("Pokemon 1:", battle_result['pokemon1']['name'], battle_result['pokemon1']['stats'])
    print("Pokemon 2:", battle_result['pokemon2']['name'], battle_result['pokemon2']['stats'])
    print("Winner:", battle_result['winner'])
