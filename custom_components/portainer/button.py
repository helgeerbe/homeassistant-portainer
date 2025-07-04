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

_LOGGER.error("=== BUTTON MODULE LOADED ===")


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button platform."""
    _LOGGER.error("=== BUTTON SETUP_ENTRY CALLED ===")
    _LOGGER.error("Config entry: %s", config_entry.entry_id)

    try:
        coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
        _LOGGER.error("Got coordinator: %s", coordinator)

        entities = []

        # Always create force update check button
        _LOGGER.error("Creating ForceUpdateCheckButton")
        button = ForceUpdateCheckButton(coordinator)
        entities.append(button)

        _LOGGER.error("Adding %d button entities", len(entities))
        if entities:
            async_add_entities(entities)
            _LOGGER.error("Button entities added successfully")
        else:
            _LOGGER.error("No button entities to add")
    except Exception as e:
        _LOGGER.error("Error setting up button platform: %s", e, exc_info=True)


class ForceUpdateCheckButton(CoordinatorEntity, ButtonEntity):
    """Button to force immediate update check."""

    def __init__(self, coordinator: PortainerCoordinator) -> None:
        """Initialize the button."""
        _LOGGER.error("Initializing ForceUpdateCheckButton")
        try:
            super().__init__(coordinator)
            self._attr_name = "Force Update Check"
            self._attr_icon = "mdi:update"
            self._attr_entity_category = "config"
            self._attr_unique_id = (
                f"{coordinator.config_entry.entry_id}_force_update_check_v2"
            )
            _LOGGER.error("Button initialized with unique_id: %s", self._attr_unique_id)
        except Exception as e:
            _LOGGER.error("Error initializing button: %s", e, exc_info=True)
            raise

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
        # Always make the button available for now to ensure it appears
        return True

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.error("Button pressed!")
        # Check if update feature is enabled before allowing press
        if not self.coordinator.features.get("feature_switch_update_check", False):
            _LOGGER.error("Update check feature is disabled, button press ignored")
            return

        _LOGGER.error("Calling force_update_check")
        await self.coordinator.force_update_check()
