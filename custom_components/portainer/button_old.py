"""Portainer button platform."""

from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import PortainerCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    # Create force update check button
    button = ForceUpdateCheckButton(coordinator)
    async_add_entities([button])


class ForceUpdateCheckButton(ButtonEntity):
    """Button to force immediate update check."""

    def __init__(self, coordinator: PortainerCoordinator) -> None:
        """Initialize the button."""
        self.coordinator = coordinator
        self._attr_name = "Force Update Check"
        self._attr_icon = "mdi:update"
        self._attr_entity_category = "config"
        # Use the original unique_id that worked before
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_force_update_check"

    @property
    def device_info(self):
        """Return device info to associate with the System device."""
        dev_connection = DOMAIN
        dev_connection_value = (
            f"{self.coordinator.name}_System_{self.coordinator.config_entry.entry_id}"
        )

        return {
            "connections": {(dev_connection, dev_connection_value)},
            "identifiers": {(dev_connection, dev_connection_value)},
            "name": f"{self.coordinator.name} System",
            "manufacturer": "Portainer",
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return True

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled when first added."""
        return self.coordinator.features.get("feature_switch_update_check", True)

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info("Force update check button pressed")
        if not self.coordinator.features.get("feature_switch_update_check", False):
            _LOGGER.warning("Update check feature is disabled")
            return

        await self.coordinator.force_update_check()
