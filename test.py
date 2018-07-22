import units
import terrains
import objects

c = units.Templars()
l = units.TwoHanded()

ctx = objects.Context(
    attacker=l,
    defender=c,
    atk_terrain=terrains.Desert(),
    dfd_terrain=terrains.Desert(),
    distance=1)

c.fight(ctx, l)
print("null")
l.fight(ctx, c)


print(c.name,c.health)
print(l.name,l.health)