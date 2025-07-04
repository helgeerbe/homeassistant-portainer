"""Portainer button platform."""

from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PortainerCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button platform."""
    _LOGGER.debug("Setting up button platform for entry %s", config_entry.entry_id)

    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    entities = []

    # Always create force update check button (it will be disabled if feature is off)
    _LOGGER.debug("Creating ForceUpdateCheckButton")
    entities.append(ForceUpdateCheckButton(coordinator))

    _LOGGER.debug("Adding %d button entities", len(entities))
    if entities:
        async_add_entities(entities)
    else:
        _LOGGER.warning("No button entities to add")


class ForceUpdateCheckButton(CoordinatorEntity, ButtonEntity):
    """Button to force immediate update check."""

    def __init__(self, coordinator: PortainerCoordinator) -> None:
        """Initialize the button."""
        _LOGGER.debug("Initializing ForceUpdateCheckButton")
        super().__init__(coordinator)
        self._attr_name = "Force Update Check"
        self._attr_icon = "mdi:update"
        self._attr_entity_category = "config"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_force_update_check"
        _LOGGER.debug("Button initialized with unique_id: %s", self._attr_unique_id)

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
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        # Button is only available if coordinator is connected AND update feature is enabled
        return self.coordinator.available and self.coordinator.features.get(
            "feature_switch_update_check", False
        )

    async def async_press(self) -> None:
        """Handle the button press."""
        # Check if update feature is enabled before allowing press
        if not self.coordinator.features.get("feature_switch_update_check", False):
            _LOGGER.warning("Update check feature is disabled, button press ignored")
            return

        await self.coordinator.force_update_check()
