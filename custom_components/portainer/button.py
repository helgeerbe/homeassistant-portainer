"""Portainer button platform."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .coordinator import PortainerCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    entities = []

    # Add force update check button if update feature is enabled
    if coordinator.features.get("feature_switch_update_check", False):
        entities.append(ForceUpdateCheckButton(coordinator))

    if entities:
        async_add_entities(entities)


class ForceUpdateCheckButton(CoordinatorEntity, ButtonEntity):
    """Button to force immediate update check."""

    def __init__(self, coordinator: PortainerCoordinator) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._attr_name = "Force Update Check"
        self._attr_icon = "mdi:update"
        self._attr_entity_category = "config"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_force_update_check"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.config_entry.entry_id)},
            "name": f"Portainer {coordinator.name}",
            "manufacturer": "Portainer",
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.available and self.coordinator.features.get(
            "feature_switch_update_check", False
        )

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.force_update_check()
