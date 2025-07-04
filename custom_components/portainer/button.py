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
        try:
            button = ForceUpdateCheckButton(coordinator)
            _LOGGER.error("Button created successfully: %s", button)
            _LOGGER.error("Button unique_id: %s", button.unique_id)
            _LOGGER.error("Button name: %s", button.name)
            entities.append(button)
            _LOGGER.error("Button added to entities list")
        except Exception as button_error:
            _LOGGER.error("Failed to create button: %s", button_error, exc_info=True)

        _LOGGER.error("Adding %d button entities", len(entities))
        if entities:
            try:
                async_add_entities(entities)
                _LOGGER.error("Button entities added successfully")
            except Exception as add_error:
                _LOGGER.error("Failed to add entities: %s", add_error, exc_info=True)
        else:
            _LOGGER.error("No button entities to add")
    except Exception as e:
        _LOGGER.error("Error setting up button platform: %s", e, exc_info=True)


class ForceUpdateCheckButton(ButtonEntity):
    """Button to force immediate update check."""

    def __init__(self, coordinator: PortainerCoordinator) -> None:
        """Initialize the button."""
        _LOGGER.error("Initializing ForceUpdateCheckButton")
        try:
            # Don't call super().__init__() for CoordinatorEntity for now
            self.coordinator = coordinator
            self._attr_name = "Force Update Check"
            self._attr_icon = "mdi:update"
            # Remove entity_category for now to see if it helps
            # self._attr_entity_category = "config"
            self._attr_unique_id = (
                f"{coordinator.config_entry.entry_id}_force_update_check_v3"
            )
            # Explicitly set entity_id to ensure it's recognized
            self.entity_id = f"button.{coordinator.name.lower().replace(' ', '_')}_force_update_check"
            _LOGGER.error("Button initialized with unique_id: %s", self._attr_unique_id)
            _LOGGER.error("Button name: %s", self._attr_name)
            _LOGGER.error("Button icon: %s", self._attr_icon)
            _LOGGER.error("Button entity_id: %s", self.entity_id)
        except Exception as e:
            _LOGGER.error("Error initializing button: %s", e, exc_info=True)
            raise

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
        # Always make the button available for now to ensure it appears
        return (
            self.coordinator.available
            if hasattr(self.coordinator, "available")
            else True
        )

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.error("Button pressed!")
        # Check if update feature is enabled before allowing press
        if not self.coordinator.features.get("feature_switch_update_check", False):
            _LOGGER.error("Update check feature is disabled, button press ignored")
            return

        _LOGGER.error("Calling force_update_check")
        await self.coordinator.force_update_check()
