import objects

def plain_charge(self, ctx, other):
    return 0.33 if ctx.def_terrain.type == objects.TerrainType.plain and ctx.status == 0 else 0

def desert_charge(self, ctx, other):
    return 0.33 if ctx.def_terrain.type == objects.TerrainType.desert and ctx.status == 0 else 0

def scared_horses(self, ctx, other):
    return 0.33 if other.type == objects.UnitType.cavalry else 0

def anti_cavalry(self, ctx, other):
    return 0.83 if other.type == objects.UnitType.cavalry else 0

def woodsmen(self, ctx, other):
    return 0.33 if ctx.def_terrain.type == objects.TerrainType.forest else 0

def volley(self, ctx, other):
    return 0.33 if self.health >= 50 else 0

ability_dict = {
    "anti-cavalry": anti_cavalry, 
    "plain charge": plain_charge, 
    "desert charge": desert_charge,
    "scared horses": scared_horses,
    "woodsmen": woodsmen,
    "volley": volley,
    "skirmish": None,
    "first strike": None,
    "berserker": None,
    "veterans": None,
    "no counter": None,
    "only buildings": None,
    "only units": None,
    "cause fear": None,
    "rapid fire": None,
    "zeal": None

}