"""Stage layouts. The other two stages are added in later project days."""

from enemy import Enemy
from objects import Coin, Platform


def build_stage_one():
    platforms = [
        Platform(0, 490, 1600, 50),
        Platform(210, 405, 150),
        Platform(440, 335, 150),
        Platform(700, 405, 170),
        Platform(1010, 350, 150),
        Platform(1270, 410, 170),
    ]
    coins = [Coin(x, y) for x, y in [(260, 370), (490, 300), (750, 370), (1060, 315), (1320, 375)]]
    enemies = [Enemy(560, 460, 520, 650)]
    stage_info = {"name": "Green Meadow", "number": 1}
    return {"platforms": platforms, "coins": coins, "enemies": enemies, "info": stage_info}

def build_stage_two():
    platforms = [
        Platform(0, 490, 1600, 50),
        Platform(170, 410, 130),
        Platform(370, 345, 140),
        Platform(610, 405, 150),
        Platform(850, 325, 140),
        Platform(1090, 395, 150),
        Platform(1360, 335, 170),
    ]

    coins = [
        Coin(x, y)
        for x, y in [
            (205, 375),
            (415, 310),
            (660, 370),
            (895, 290),
            (1135, 360),
            (1415, 300),
        ]
    ]

    enemies = [
        Enemy(520, 460, 470, 590),
        Enemy(1030, 460, 970, 1080),
    ]

    stage_info = {"name": "Moonlit Cave", "number": 2}

    return {
        "platforms": platforms,
        "coins": coins,
        "enemies": enemies,
        "info": stage_info,
    }