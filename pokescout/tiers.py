"""Popularność Pokémonów i wagi rzadkości.

Lista startowa jest subiektywna — po zebraniu danych warto ją skalibrować
(np. medianą cen kart Illustration Rare / SIR danego Pokémona albo Google Trends).
"""

# Tier 1: Pokémony, na których karty popyt utrzymuje się od lat
TIER_1 = {
    "pikachu", "charizard", "umbreon", "eevee", "mew", "mewtwo", "gengar",
    "lugia", "rayquaza", "sylveon", "espeon", "greninja", "gardevoir",
    "snorlax", "magikarp", "gyarados", "blastoise", "venusaur",
}

# Tier 2: mocni ulubieńcy fanów
TIER_2 = {
    "vaporeon", "jolteon", "flareon", "leafeon", "glaceon", "dragonite",
    "lucario", "ho-oh", "celebi", "jirachi", "darkrai", "giratina", "arceus",
    "bulbasaur", "squirtle", "charmander", "psyduck", "ninetales", "vulpix",
    "arcanine", "mimikyu", "tyranitar", "garchomp", "metagross", "zoroark",
    "lapras", "articuno", "zapdos", "moltres", "suicune", "latias", "latios",
    "dragapult", "ditto", "jigglypuff", "piplup", "cubone", "lycanroc",
    # trenerzy (karty Supporter w wersji SIR mają osobny, silny popyt)
    "lillie", "iono", "marnie", "erika", "misty", "cynthia", "serena", "n",
}

TIER_SCORE = {1: 1.0, 2: 0.7, 3: 0.35}

# Waga rzadkości (0–1). Klucze po normalizacji do małych liter.
RARITY_WEIGHT = {
    "special illustration rare": 1.0,
    "alternate art": 1.0,          # alt arty z ery Sword & Shield
    "classic collection": 0.9,     # klasyczne dodruki w złotej ramce
    "hyper rare": 0.75,            # złote karty
    "illustration rare": 0.8,
    "ultra rare": 0.5,             # full arty
    "double rare": 0.2,
    "rare holo": 0.15,
    # nazwy rzadkości używane przez pokemontcg.io (era Sword & Shield i starsze).
    # „Rare Secret” obejmuje alt arty, ale też złote i tęczowe karty – API ich nie rozróżnia.
    "rare secret": 0.85,
    "rare rainbow": 0.6,
    "rare ultra": 0.5,
    "trainer gallery rare holo": 0.6,
    "rare holo vmax": 0.4,
    "rare holo vstar": 0.4,
    "shiny rare": 0.5,
    "shiny ultra rare": 0.6,
    "rare shiny gx": 0.6,
    "rare shining": 0.7,
}


def pokemon_tier(name: str) -> int:
    """Zwraca tier (1–3) na podstawie nazwy karty, np. 'Umbreon VMAX' -> 1."""
    tokens = (
        name.lower()
        .replace("'s", "")
        .replace("&", " ")
        .replace("-ex", " ")
        .split()
    )
    # "Ho-Oh" ma myślnik w nazwie, więc sprawdzamy też całą frazę
    lowered = name.lower()
    best = 3
    for t in tokens + [lowered]:
        if t in TIER_1:
            return 1
        if t in TIER_2:
            best = 2
    if "ho-oh" in lowered:
        best = min(best, 2)
    return best


def rarity_weight(rarity: str) -> float:
    return RARITY_WEIGHT.get((rarity or "").strip().lower(), 0.1)
