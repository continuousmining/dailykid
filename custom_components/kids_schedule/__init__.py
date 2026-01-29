"""The Kids Schedule integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    CONF_ALEXA_ENTITY,
    CONF_ANNOUNCEMENT_ENABLED,
    CONF_TASK_COMPLETE_ANNOUNCEMENT,
    CONF_ROUTINE_START_ANNOUNCEMENT,
    CONF_ROUTINE_COMPLETE_ANNOUNCEMENT,
    SERVICE_CHECK_TASK,
    SERVICE_UNCHECK_TASK,
    SERVICE_RESET_ROUTINE,
    SERVICE_ANNOUNCE,
    ATTR_ROUTINE_ID,
    ATTR_TASK_INDEX,
    ATTR_MESSAGE,
    EVENT_ROUTINE_STARTED,
    EVENT_TASK_COMPLETED,
    EVENT_ROUTINE_COMPLETED,
)
from .coordinator import KidsScheduleCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

# Service schemas
CHECK_TASK_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_ROUTINE_ID): cv.string,
        vol.Required(ATTR_TASK_INDEX): cv.positive_int,
    }
)

UNCHECK_TASK_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_ROUTINE_ID): cv.string,
        vol.Required(ATTR_TASK_INDEX): cv.positive_int,
    }
)

RESET_ROUTINE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_ROUTINE_ID): cv.string,
    }
)

ANNOUNCE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_MESSAGE): cv.string,
    }
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Kids Schedule from a config entry."""
    coordinator = KidsScheduleCoordinator(hass, entry)
    
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services
    async def handle_check_task(call: ServiceCall) -> None:
        """Handle check task service call."""
        routine_id = call.data[ATTR_ROUTINE_ID]
        task_index = call.data[ATTR_TASK_INDEX]

        try:
            await coordinator.async_check_task(routine_id, task_index)

            # Fire event
            hass.bus.async_fire(
                EVENT_TASK_COMPLETED,
                {
                    ATTR_ROUTINE_ID: routine_id,
                    ATTR_TASK_INDEX: task_index,
                },
            )

            # Announce if enabled
            if entry.data.get(CONF_ANNOUNCEMENT_ENABLED) and entry.data.get(
                CONF_TASK_COMPLETE_ANNOUNCEMENT
            ):
                routine = coordinator.data["daily"].get(routine_id)
                if routine:
                    completed = routine["completed_count"]
                    total = routine["total_count"]
                    
                    if completed == total:
                        # Routine complete
                        message = f"Great job! You finished {routine['title']}!"
                        if entry.data.get(CONF_ROUTINE_COMPLETE_ANNOUNCEMENT):
                            await announce_message(hass, entry, message)
                    else:
                        # Task complete
                        message = f"Nice work! {completed} of {total} tasks done."
                        await announce_message(hass, entry, message)

        except ValueError as err:
            _LOGGER.error("Error checking task: %s", err)

    async def handle_uncheck_task(call: ServiceCall) -> None:
        """Handle uncheck task service call."""
        routine_id = call.data[ATTR_ROUTINE_ID]
        task_index = call.data[ATTR_TASK_INDEX]

        try:
            await coordinator.async_uncheck_task(routine_id, task_index)
        except ValueError as err:
            _LOGGER.error("Error unchecking task: %s", err)

    async def handle_reset_routine(call: ServiceCall) -> None:
        """Handle reset routine service call."""
        routine_id = call.data[ATTR_ROUTINE_ID]

        try:
            await coordinator.async_reset_routine(routine_id)
        except ValueError as err:
            _LOGGER.error("Error resetting routine: %s", err)

    async def handle_announce(call: ServiceCall) -> None:
        """Handle announce service call."""
        message = call.data[ATTR_MESSAGE]
        await announce_message(hass, entry, message)

    # Register services for this config entry
    hass.services.async_register(
        DOMAIN, SERVICE_CHECK_TASK, handle_check_task, schema=CHECK_TASK_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_UNCHECK_TASK, handle_uncheck_task, schema=UNCHECK_TASK_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_RESET_ROUTINE, handle_reset_routine, schema=RESET_ROUTINE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_ANNOUNCE, handle_announce, schema=ANNOUNCE_SCHEMA
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def announce_message(
    hass: HomeAssistant, entry: ConfigEntry, message: str
) -> None:
    """Send announcement to Alexa device."""
    alexa_entity = entry.data.get(CONF_ALEXA_ENTITY) or entry.options.get(
        CONF_ALEXA_ENTITY
    )

    if not alexa_entity:
        _LOGGER.debug("No Alexa entity configured, skipping announcement")
        return

    if not entry.data.get(CONF_ANNOUNCEMENT_ENABLED, True):
        _LOGGER.debug("Announcements disabled, skipping")
        return

    try:
        # Try Alexa Media Player notify service first
        await hass.services.async_call(
            "notify",
            alexa_entity.replace("media_player.", "alexa_media_"),
            {
                "message": message,
                "data": {"type": "announce"},
            },
        )
    except Exception:
        # Fallback to TTS
        try:
            await hass.services.async_call(
                "tts",
                "speak",
                {
                    "entity_id": alexa_entity,
                    "message": message,
                },
            )
        except Exception as err:
            _LOGGER.warning("Error sending announcement: %s", err)
