from ..components.ai import HostileEnemy
from ..components.consumable import *
from ..components.equippable import *
from ..components.equipment import Equipment
from ..components.fighter import Fighter
from ..components.inventory import Inventory
from ..components.level import Level
from .entity import Actor, Item

player = Actor(char="@", color=(255, 255, 255), name="Player", ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(hp=30, base_defense=1, base_power=2), inventory=Inventory(capacity=26), level=Level(level_up_base=200))
# Monsters
orc = Actor(char="o", color=(63, 127, 63), name="Orc", ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(hp=10, base_defense=0, base_power=3), inventory=Inventory(capacity=0), level=Level(xp_given=35))
troll = Actor(char="T", color=(0, 127, 0), name="Troll", ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(hp=16, base_defense=1, base_power=4), inventory=Inventory(capacity=0), level=Level(xp_given=100))
# Items
health_potion = Item(char="!", color=(127, 0, 255), name="Health Potion", consumable=HealingConsumable(amount=4))
# Scrolls
confusion_scroll = Item(char="~", color=(207, 63, 255), name="Confusion Scroll", consumable=ConfusionConsumable(number_of_turns=10))
fireball_scroll = Item(char="~", color=(255, 0, 0), name="Fireball Scroll", consumable=FireballDamageConsumable(damage=15, radius=3))
lightning_scroll = Item(char="~", color=(255, 255, 0), name="Lightning Scroll", consumable=LightningDamageConsumable(damage=30, maximum_range=5))
# Weapons/Equipment
dagger = Item(char="/", color=(0, 191, 255), name="Dagger", equippable=Dagger())
sword = Item(char="/", color=(0, 191, 255), name="Sword", equippable=Sword())
leather_armor = Item(char="[", color=(139, 69, 19), name="Leather Armor", equippable=LeatherArmor())
chain_mail = Item(char="[", color=(139, 69, 19), name="Chain Mail", equippable=ChainMail())
