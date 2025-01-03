from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..dungeongame.actions import *
from ..dungeongame.color import *
from .base_component import BaseComponent
from inventory import Inventory
from ..dungeongame.exceptions import Impossible

if TYPE_CHECKING:
    from ..dungeongame.entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Actor) -> Optional[Action]:
        return ItemAction(consumer, self.parent)

    def activate(self, action: ItemAction) -> None:
        raise NotImplementedError()

    def consume(self) -> None:
        """Remove the consumed item from its containing inventory."""
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, Inventory):
            inventory.items.remove(entity)


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)
        if amount_recovered > 0:
            self.engine.message_log.add_message(f"You consume the {self.parent.name}, and recover {amount_recovered} HP!", health_recovered)
            self.consume()
        else:
            raise Impossible("Your health is already full.")
