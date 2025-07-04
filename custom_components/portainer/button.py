"""Portainer button platform."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_FEATURE_UPDATE_CHECK, DOMAIN
from .coordinator import PortainerCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    entities = []

    # DEBUG: Add force update check button always for testing
    entities.append(ForceUpdateCheckButton(coordinator))
    # TODO: Change to: if coordinator.features.get(CONF_FEATURE_UPDATE_CHECK, False):

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

    @property
    def device_info(self):
        """Return device info to associate with the same device as containers."""
        # Get the first available endpoint ID to match container device grouping
        endpoint_id = None
        if "endpoints" in self.coordinator.data and self.coordinator.data["endpoints"]:
            endpoint_id = next(iter(self.coordinator.data["endpoints"].keys()))

        if endpoint_id:
            # Match exactly what PortainerEntity does for ha_group="data__EndpointId"
            dev_connection = DOMAIN
            dev_connection_value = endpoint_id

            # make connection unique across configurations
            dev_connection_value += f"_{self.coordinator.config_entry.entry_id}"

            return {
                "connections": {(dev_connection, dev_connection_value)},
                "identifiers": {(dev_connection, dev_connection_value)},
                "default_name": f"{self.coordinator.name} {endpoint_id}",
                "default_manufacturer": "Docker",
            }
        else:
            # Fallback to endpoints device if no endpoint ID available
            dev_connection = DOMAIN
            dev_connection_value = f"{self.coordinator.name}_Endpoints_{self.coordinator.config_entry.entry_id}"

            return {
                "connections": {(dev_connection, dev_connection_value)},
                "identifiers": {(dev_connection, dev_connection_value)},
                "default_name": f"{self.coordinator.name} Endpoints",
                "default_manufacturer": "Docker",
            }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.available

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.force_update_check()
