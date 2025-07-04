"""Minimal button platform for debugging."""

import logging

_LOGGER = logging.getLogger(__name__)
_LOGGER.error("=== BUTTON MODULE LOADED ===")


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up button platform - minimal version."""
    _LOGGER.error("=== BUTTON SETUP_ENTRY CALLED ===")
    _LOGGER.error("Config entry: %s", config_entry.entry_id)
    _LOGGER.error("Hass: %s", hass)
    _LOGGER.error("Add entities callback: %s", async_add_entities)

    # Don't add any entities for now, just confirm this is called
    _LOGGER.error("=== BUTTON SETUP_ENTRY FINISHED ===")
