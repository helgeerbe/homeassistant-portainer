"""Portainer button platform."""

from __future__ import annotations
from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_FEATURE_UPDATE_CHECK
from .coordinator import PortainerCoordinator
from .entity import PortainerEntity


@dataclass
class ButtonDescription:
    """Mock description for button entities."""

    ha_group: str = "System"
    data_attributes_list: list | None = None

    def __post_init__(self):
        if self.data_attributes_list is None:
            self.data_attributes_list = []


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    entities = []

    # Add force update check button if update feature is enabled
    if coordinator.features.get(CONF_FEATURE_UPDATE_CHECK, False):
        entities.append(ForceUpdateCheckButton(coordinator))

    if entities:
        async_add_entities(entities)


class ForceUpdateCheckButton(PortainerEntity, ButtonEntity):
    """Button to force immediate update check."""

    def __init__(self, coordinator: PortainerCoordinator) -> None:
        """Initialize the button."""
        # Create a mock description for PortainerEntity
        description = ButtonDescription()
        super().__init__(coordinator, description)
        self._attr_name = "Force Update Check"
        self._attr_icon = "mdi:update"
        self._attr_entity_category = "config"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_force_update_check"

    # Implement abstract methods from PortainerEntity (not used for buttons)
    async def start(self):
        """Not applicable for button."""
        return

    async def stop(self):
        """Not applicable for button."""
        return

    async def restart(self):
        """Not applicable for button."""
        return

    async def reload(self):
        """Not applicable for button."""
        return

    async def snapshot(self):
        """Not applicable for button."""
        return

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.available and self.coordinator.features.get(
            CONF_FEATURE_UPDATE_CHECK, False
        )

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.force_update_check()
