import objects

class Desert(objects.Terrain):
    def __init__(self):
        super().__init__(
            movement_cost = 2,
            vision_cost = 2,
            type = objects.TerrainType.desert,
        )

class DesertRoad(objects.Terrain):
    def __init__(self):
        super().__init__(
            movement_cost = 1,
            vision_cost = 2,
            type = objects.TerrainType.desert,
            sub_type = objects.TerrainSubType.road
        )

class Plain(objects.Terrain):
    def __init__(self):
        super().__init__(
            movement_cost = 2,
            vision_cost = 2,
            type = objects.TerrainType.plain,
        )

class PlainRoad(objects.Terrain):
    def __init__(self):
        super().__init__(
            movement_cost = 1,
            vision_cost = 2,
            type = objects.TerrainType.plain,
            sub_type = objects.TerrainSubType.road
        )

class Forest(objects.Terrain):
    def __init__(self):
        super().__init__(
            movement_cost = 3,
            vision_cost = 3,
            defense_bonus = 0.2,
            range_bonus = -1,
            type = objects.TerrainType.forest
        )

class Mountain(objects.Terrain):
    def __init__(self):
        super().__init__(
            movement_cost = 4,
            vision_cost = 4,
            defense_bonus = 0.4,
            range_bonus = 1,
            vision_bonus = 4,
            type = objects.TerrainType.mountain
        )

class MountainRoad(objects.Terrain):
    def __init__(self):
        super().__init__(
            movement_cost = 3,
            vision_cost = 4,
            defense_bonus = 0.4,
            range_bonus = 1,
            vision_bonus = 4,
            type = objects.TerrainType.mountain,
            sub_type = objects.TerrainSubType.road
        )

class Swamp(objects.Terrain):
    def __init__(self):
        super().__init__(
            movement_cost = 3,
            vision_cost = 3,
            defense_bonus = 0.2,
            range_bonus = -1,
            type = objects.TerrainType.swamp
        )

class Hill(objects.Terrain):
    def __init__(self):
        super().__init__(
            movement_cost = 3,
            vision_cost = 2,
            defense_bonus = 0.2,
            range_bonus = 1,
            type = objects.TerrainType.hill
        )

class HillRoad(objects.Terrain):
    def __init__(self):
        super().__init__(
            movement_cost = 2,
            vision_cost = 2,
            defense_bonus = 0.2,
            range_bonus = 1,
            type = objects.TerrainType.hill,
            sub_type = objects.TerrainSubType.road
        )

class Ford(objects.Terrain):
    def __init__(self):
        super().__init__(
            movement_cost = 3,
            vision_cost = 2,
            defense_bonus = 0.2,
            type = objects.TerrainType.ford
        )

class Bridge(objects.Terrain):
    def __init__(self):
        super().__init__(
            movement_cost = 2,
            vision_cost = 2,
            defense_bonus = 0.4,
            type = objects.TerrainType.bridge
        )
