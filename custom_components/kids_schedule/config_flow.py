"""Config flow for Kids Schedule integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_CALENDAR_ENTITY,
    CONF_ALEXA_ENTITY,
    CONF_ANNOUNCEMENT_ENABLED,
    CONF_TASK_COMPLETE_ANNOUNCEMENT,
    CONF_ROUTINE_START_ANNOUNCEMENT,
    CONF_ROUTINE_COMPLETE_ANNOUNCEMENT,
    CONF_RESET_TIME,
    CONF_REQUIRE_ORDER,
    DEFAULT_ANNOUNCEMENT_ENABLED,
    DEFAULT_TASK_COMPLETE,
    DEFAULT_ROUTINE_START,
    DEFAULT_ROUTINE_COMPLETE,
    DEFAULT_RESET_TIME,
    DEFAULT_REQUIRE_ORDER,
)


class KidsScheduleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Kids Schedule."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate calendar entity exists
            calendar_entity = user_input[CONF_CALENDAR_ENTITY]
            if not self.hass.states.get(calendar_entity):
                errors[CONF_CALENDAR_ENTITY] = "invalid_calendar"
            
            # Validate Alexa entity if provided
            alexa_entity = user_input.get(CONF_ALEXA_ENTITY)
            if alexa_entity and not self.hass.states.get(alexa_entity):
                errors[CONF_ALEXA_ENTITY] = "invalid_alexa"
            
            if not errors:
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default="Kids Schedule"): str,
                vol.Required(CONF_CALENDAR_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="calendar")
                ),
                vol.Optional(CONF_ALEXA_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="media_player")
                ),
                vol.Optional(
                    CONF_ANNOUNCEMENT_ENABLED, 
                    default=DEFAULT_ANNOUNCEMENT_ENABLED
                ): bool,
                vol.Optional(
                    CONF_ROUTINE_START_ANNOUNCEMENT,
                    default=DEFAULT_ROUTINE_START
                ): bool,
                vol.Optional(
                    CONF_TASK_COMPLETE_ANNOUNCEMENT,
                    default=DEFAULT_TASK_COMPLETE
                ): bool,
                vol.Optional(
                    CONF_ROUTINE_COMPLETE_ANNOUNCEMENT,
                    default=DEFAULT_ROUTINE_COMPLETE
                ): bool,
                vol.Optional(
                    CONF_RESET_TIME,
                    default=DEFAULT_RESET_TIME
                ): selector.TimeSelector(),
                vol.Optional(
                    CONF_REQUIRE_ORDER,
                    default=DEFAULT_REQUIRE_ORDER
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> KidsScheduleOptionsFlowHandler:
        """Get the options flow for this handler."""
        return KidsScheduleOptionsFlowHandler(config_entry)


class KidsScheduleOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Kids Schedule."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_ALEXA_ENTITY,
                    default=self.config_entry.options.get(CONF_ALEXA_ENTITY, "")
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="media_player")
                ),
                vol.Optional(
                    CONF_ANNOUNCEMENT_ENABLED,
                    default=self.config_entry.options.get(
                        CONF_ANNOUNCEMENT_ENABLED, DEFAULT_ANNOUNCEMENT_ENABLED
                    ),
                ): bool,
                vol.Optional(
                    CONF_ROUTINE_START_ANNOUNCEMENT,
                    default=self.config_entry.options.get(
                        CONF_ROUTINE_START_ANNOUNCEMENT, DEFAULT_ROUTINE_START
                    ),
                ): bool,
                vol.Optional(
                    CONF_TASK_COMPLETE_ANNOUNCEMENT,
                    default=self.config_entry.options.get(
                        CONF_TASK_COMPLETE_ANNOUNCEMENT, DEFAULT_TASK_COMPLETE
                    ),
                ): bool,
                vol.Optional(
                    CONF_ROUTINE_COMPLETE_ANNOUNCEMENT,
                    default=self.config_entry.options.get(
                        CONF_ROUTINE_COMPLETE_ANNOUNCEMENT, DEFAULT_ROUTINE_COMPLETE
                    ),
                ): bool,
                vol.Optional(
                    CONF_RESET_TIME,
                    default=self.config_entry.options.get(
                        CONF_RESET_TIME, DEFAULT_RESET_TIME
                    ),
                ): selector.TimeSelector(),
                vol.Optional(
                    CONF_REQUIRE_ORDER,
                    default=self.config_entry.options.get(
                        CONF_REQUIRE_ORDER, DEFAULT_REQUIRE_ORDER
                    ),
                ): bool,
            }
        )

        return self.async_show_form(step_id="init", data_schema=options_schema)
