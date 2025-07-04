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
    _LOGGER.error("=== BUTTON SETUP START ===")
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    _LOGGER.error("Got coordinator: %s", coordinator)
    
    button = ForceUpdateCheckButton(coordinator)
    _LOGGER.error("Button created: %s", button)
    _LOGGER.error("Button unique_id: %s", button.unique_id)
    _LOGGER.error("Button available: %s", button.available)
    _LOGGER.error("Button enabled_default: %s", button.entity_registry_enabled_default)
    
    entities = [button]
    async_add_entities(entities)
    _LOGGER.error("=== BUTTON SETUP COMPLETE ===")


class ForceUpdateCheckButton(ButtonEntity):
    """Button to force immediate update check."""

    def __init__(self, coordinator: PortainerCoordinator) -> None:
        """Initialize the button."""
        _LOGGER.error("=== BUTTON INIT START ===")
        self.coordinator = coordinator
        self._attr_name = "Force Update Check"
        self._attr_icon = "mdi:update"
        self._attr_entity_category = "config"
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_force_update_check_v4"
        )
        _LOGGER.error("Button init complete - unique_id: %s", self._attr_unique_id)

    @property
    def name(self) -> str:
        """Return the name of the button."""
        return self._attr_name

    @property
    def unique_id(self) -> str:
        """Return unique ID for the button."""
        return self._attr_unique_id

    @property
    def icon(self) -> str:
        """Return the icon for the button."""
        return self._attr_icon

    @property
    def device_info(self):
        """Return device info to associate with the System device."""
        # Match exactly what PortainerEntity does for ha_group="System"
        dev_connection = DOMAIN
        dev_connection_value = (
            f"{self.coordinator.name}_System_{self.coordinator.config_entry.entry_id}"
        )

        return {
            "connections": {(dev_connection, dev_connection_value)},
            "identifiers": {(dev_connection, dev_connection_value)},
            "name": f"{self.coordinator.name} System",
            "manufacturer": "Portainer",
            "sw_version": getattr(self.coordinator, "sw_version", "Unknown"),
            "configuration_url": f"http{'s' if self.coordinator.config_entry.data.get('ssl', False) else ''}://{self.coordinator.config_entry.data.get('host', 'localhost')}",
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        # Always available for now - we'll control via enabled state
        return self.coordinator.available

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled when first added."""
        return self.coordinator.features.get("feature_switch_update_check", False)

    async def async_press(self) -> None:
        """Handle the button press."""
        if not self.coordinator.features.get("feature_switch_update_check", False):
            _LOGGER.warning("Update check feature is disabled")
            return

        await self.coordinator.force_update_check()
