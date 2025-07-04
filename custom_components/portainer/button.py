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
    _LOGGER.warning(
        "Setting up Portainer button platform - button entity will be created"
    )
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    button = ForceUpdateCheckButton(coordinator, config_entry.entry_id)
    async_add_entities([button])
    _LOGGER.warning("Portainer button entity created and added: %s", button.unique_id)


class ForceUpdateCheckButton(ButtonEntity):
    """Button to force immediate update check."""

    def __init__(self, coordinator: PortainerCoordinator, entry_id: str) -> None:
        """Initialize the button."""
        self.coordinator = coordinator
        self.entry_id = entry_id

        # Set basic attributes
        self._attr_name = "Force Update Check"
        self._attr_icon = "mdi:update"
        self._attr_unique_id = f"{entry_id}_force_update_check_final"

        _LOGGER.warning(
            "Force Update Check button initialized with unique_id: %s",
            self._attr_unique_id,
        )

    @property
    def device_info(self):
        """Return device info to group with System device."""
        return {
            "identifiers": {
                (DOMAIN, f"{self.coordinator.name}_System_{self.entry_id}")
            },
            "name": f"{self.coordinator.name} System",
            "manufacturer": "Portainer",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        # Test logging to verify it works
        _LOGGER.warning("BUTTON PRESSED - Force Update Check button pressed!")
        _LOGGER.info(
            "Force Update Check button pressed - initiating immediate update check for all containers"
        )
        await self.coordinator.force_update_check()
