import enum
import abilities
from simpleeval import simple_eval
import sys

class Unit:
    def __init__(self, **kwargs):
        self.name = kwargs["name"] if "name" in kwargs else self.__class__.__name__
        self.health = kwargs["health"] if "health" in kwargs else 100
        self.movement = kwargs["movement"]
        self.attack = kwargs["attack"]
        self.defense = kwargs["defense"]
        self.vision = kwargs["vision"]
        self.type = kwargs["type"]
        self.range = kwargs["range"]
        self.battles = kwargs["battles"] if "battles" in kwargs else 0
        self.abilities = kwargs["abilities"] if "abilities" in kwargs else []
        self.def_upgrade = kwargs["def_upgrade"] if "def_upgrade" in kwargs else False
        self.atk_upgrade = kwargs["atk_upgrade"] if "atk_upgrade" in kwargs else False

    def __str__(self):
        return f"<{self.name} health={self.health} battles={self.battles}>"

    def set(self, attr, value):
        self.__setattr__(attr, value)

    def percent(self):
        if "berserker" in self.abilities:
            return 1

        return self.health / 100 if self.health <= 100 else 1

    def ribbons(self):
        if "veteran" in self.abilities:
            return ((self.battles // 2) * 0.15) if self.battles < 6 else 0.45

        return ((self.battles // 3) * 0.15) if self.battles < 9 else 0.45

    @property   
    def armor_upgrade(self):
        return 0.25 if self.def_upgrade else 0

    @property
    def weapon_upgrade(self):
        return 0.25 if self.atk_upgrade else 0

    def process_abilities(self, ctx, other):
        env = {
            "other": other,
            "ctx": ctx,
            "self": self,
            "objects": sys.modules["objects"],
            "UnitType": UnitType,
            "TerrainType": TerrainType,
            "TerrainSubType": TerrainSubType
        }

        abilities_modif = 0
        for ability in self.abilities:
            try:
                abilities_modif += abilities.ability_dict[ability](self, ctx, other)
            except KeyError:
                abilities_modif += simple_eval(ctx.custom_abilities[ability], names=env)
            except TypeError:
                pass

        return abilities_modif

    def fight(self, ctx, other):
        if self.health <= 0:
            return

        if "no counter" in self.abilities and ctx.status == 1:
            return

        if "only buildings" in self.abilities and other.type != UnitType.structure:
            return

        if "only units" in self.abilities and other.type == UnitType.structure:
            return

        if (ctx.distance == 1 and ctx.status == 0) or (ctx.distance > 1 and ctx.status == 0):
            terrain_bonus = ctx.def_terrain.def_bonus
        elif ctx.distance > 1 and ctx.status == 1:
            terrain_bonus = ctx.atk_terrain.def_bonus
        else:
            terrain_bonus = 0

        atk_modif = 1 + bonus_dict[self.type][other.type] + self.ribbons() + self.process_abilities(ctx, other) + self.weapon_upgrade
        attack_nopercent = self.attack * atk_modif
        attack = attack_nopercent * self.percent()

        def_modif = 1 + bonus_dict[other.type][self.type] + other.ribbons() + other.process_abilities(ctx, self) + other.armor_upgrade + terrain_bonus
        defense_nopercent = other.defense * def_modif
        defense = defense_nopercent * other.percent()

        if "cause fear" in self.abilities:
            defense -= other.defense * 0.25

        if "cause fear" in other.abilities:
            attack -= self.attack * 0.25

        lost_h = round((attack / (defense * 2)) * 100)

        print(f"real attack of {self.name}: {attack} - modifier: {atk_modif} - net atk: {round(attack_nopercent)}")
        if ctx.debug:
            print(f"net atk: {self.attack * atk_modif} \n{bonus_dict[self.type][other.type]} + {self.ribbons()} + {self.process_abilities(ctx, other)} + {self.weapon_upgrade}")

        print(f"real defense of {other.name}: {defense} - modifier: {def_modif} - net def {round(defense_nopercent)}")
        if ctx.debug:
            print(f"net defense {other.defense * def_modif} \n{bonus_dict[other.type][self.type]} + {other.ribbons()} + {other.process_abilities(ctx, self)} + {other.armor_upgrade} + {terrain_bonus}")

        print(f"health lost {lost_h}")
        print("")

        if lost_h > other.health:
            lost_h = other.health

        other.health -= lost_h

        if self.health > 100:
            self.health = 100

        if other.health > 100:
            other.health = 100

class Terrain:
    def __init__(self, **kwargs):
        self.name = kwargs["name"] if "name" in kwargs else self.__class__.__name__
        self.mov_cost = kwargs["mov_cost"]
        self.vis_cost = kwargs["vis_cost"]
        self.def_bonus = kwargs["def_bonus"] if "defense_bonus" in kwargs else 0
        self.rng_bonus = kwargs["rng_bonus"] if "range_bonus" in kwargs else 0
        self.vis_bonus = kwargs["vis_bonus"] if "vision_bonus" in kwargs else 0
        self.type = kwargs["type"]
        self.sub_type = kwargs["sub_type"] if "sub_type" in kwargs else TerrainSubType.normal
        self.structure = kwargs["structure"] if "structure" in kwargs else False

    def __str__(self):
        return f"{self.type}({self.sub_type})"

    def set(self, attr, value):
        self.__setattr__(attr, value)

class UnitType(enum.Enum):
    infantry  = 0
    ranged    = 1
    cavalry   = 2
    siege     = 3
    structure = 4

class TerrainType(enum.Enum):
    plain     = 0
    desert    = 1
    structure = 2
    hill      = 3
    mountain  = 4
    forest    = 5
    swamp     = 6
    bridge    = 7
    ford      = 8

class TerrainSubType(enum.Enum):
    normal = 0
    road   = 1

class Context:
    def __init__(self, **kwargs):
        self.attacker = kwargs["attacker"]
        self.defender = kwargs["defender"]
        self.atk_terrain = kwargs["atk_terrain"]
        self.def_terrain = kwargs["def_terrain"]
        self.status = 0 #0 attack 1 counter attack
        self.distance = kwargs["distance"]
        self.debug = kwargs["debug"]
        self.custom_abilities = kwargs["custom_abilities"]


bonus_dict = {
    UnitType.infantry:  {UnitType.infantry: 0,    UnitType.ranged: 0,    UnitType.cavalry: 0, UnitType.siege: 0.33, UnitType.structure: 0.33}, 
    UnitType.ranged:    {UnitType.infantry: 0,    UnitType.ranged: 0,    UnitType.cavalry: 0, UnitType.siege: 0,    UnitType.structure: -0.5},
    UnitType.cavalry:   {UnitType.infantry: 0.33, UnitType.ranged: 0.33, UnitType.cavalry: 0, UnitType.siege: 0,    UnitType.structure: -0.5},
    UnitType.siege:     {UnitType.infantry: 0,    UnitType.ranged: 0,    UnitType.cavalry: 0, UnitType.siege: 0,    UnitType.structure: -0.5},
    UnitType.structure: {UnitType.infantry: 0,    UnitType.ranged: 0,    UnitType.cavalry: 0, UnitType.siege: 0,    UnitType.structure:0}
}
