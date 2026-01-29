"""Data coordinator for Kids Schedule."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
from typing import Any

import yaml

from homeassistant.components.calendar import CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, Event
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    CONF_CALENDAR_ENTITY,
    STORAGE_KEY,
    STORAGE_VERSION,
    ATTR_TASKS,
    ATTR_IMAGE,
    ATTR_DURATION,
    ATTR_START_TIME,
    ATTR_END_TIME,
    ATTR_ROUTINE_ID,
)

_LOGGER = logging.getLogger(__name__)


class KidsScheduleCoordinator(DataUpdateCoordinator):
    """Coordinator to manage Kids Schedule data."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
        )
        self.config_entry = config_entry
        self.calendar_entity = config_entry.data[CONF_CALENDAR_ENTITY]
        self._store = Store(hass, STORAGE_VERSION, f"{STORAGE_KEY}_{config_entry.entry_id}")
        self._state: dict[str, dict[str, Any]] = {}
        self._routines_cache: dict[str, dict[str, Any]] = {}

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from calendar and merge with completion state."""
        try:
            # Load stored state
            if not self._state:
                stored_data = await self._store.async_load()
                if stored_data:
                    self._state = stored_data.get("routines", {})

            # Get today's events
            now = dt_util.now()
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)

            # Get events from calendar
            calendar_events = await self._get_calendar_events(start_of_day, end_of_day)
            
            # Get weekly events (7 days)
            end_of_week = start_of_day + timedelta(days=7)
            weekly_events = await self._get_calendar_events(start_of_day, end_of_week)

            # Parse routines from events
            daily_routines = self._parse_routines(calendar_events, now)
            weekly_routines = self._parse_routines_weekly(weekly_events)

            # Merge with completion state
            for routine_id, routine in daily_routines.items():
                if routine_id in self._state:
                    # Restore completion state
                    state_tasks = self._state[routine_id].get("tasks", [])
                    for i, task in enumerate(routine.get("tasks", [])):
                        if i < len(state_tasks):
                            task["completed"] = state_tasks[i].get("completed", False)

            return {
                "daily": daily_routines,
                "weekly": weekly_routines,
                "current_routine": self._get_current_routine(daily_routines, now),
                "next_routine": self._get_next_routine(daily_routines, now),
            }

        except Exception as err:
            _LOGGER.error("Error updating Kids Schedule data: %s", err)
            raise UpdateFailed(f"Error fetching data: {err}") from err

    async def _get_calendar_events(
        self, start: datetime, end: datetime
    ) -> list[CalendarEvent]:
        """Get calendar events for a date range."""
        try:
            # Call calendar.get_events service
            response = await self.hass.services.async_call(
                "calendar",
                "get_events",
                {
                    "entity_id": self.calendar_entity,
                    "start_date_time": start.isoformat(),
                    "end_date_time": end.isoformat(),
                },
                blocking=True,
                return_response=True,
            )
            
            events = response.get(self.calendar_entity, {}).get("events", [])
            return events

        except Exception as err:
            _LOGGER.error("Error getting calendar events: %s", err)
            return []

    def _parse_routines(
        self, events: list[dict], now: datetime
    ) -> dict[str, dict[str, Any]]:
        """Parse calendar events into routine structure."""
        routines = {}

        for event in events:
            try:
                routine_id = self._generate_routine_id(event)
                
                # Parse YAML from description
                description = event.get("description", "")
                tasks = self._parse_tasks_from_description(description)

                if not tasks:
                    continue

                start = dt_util.parse_datetime(event["start"])
                end = dt_util.parse_datetime(event["end"])

                routines[routine_id] = {
                    "id": routine_id,
                    "title": event.get("summary", "Routine"),
                    "start_time": start,
                    "end_time": end,
                    "is_current": start <= now <= end,
                    "tasks": tasks,
                    "completed_count": sum(1 for t in tasks if t.get("completed", False)),
                    "total_count": len(tasks),
                }

            except Exception as err:
                _LOGGER.warning("Error parsing routine from event: %s", err)
                continue

        return routines

    def _parse_routines_weekly(self, events: list[dict]) -> dict[str, list[dict]]:
        """Parse events into weekly structure grouped by day."""
        weekly = {}

        for event in events:
            try:
                start = dt_util.parse_datetime(event["start"])
                day_key = start.strftime("%Y-%m-%d")

                if day_key not in weekly:
                    weekly[day_key] = []

                routine_id = self._generate_routine_id(event)
                description = event.get("description", "")
                tasks = self._parse_tasks_from_description(description)

                weekly[day_key].append({
                    "id": routine_id,
                    "title": event.get("summary", "Routine"),
                    "start_time": start,
                    "end_time": dt_util.parse_datetime(event["end"]),
                    "task_count": len(tasks),
                })

            except Exception as err:
                _LOGGER.warning("Error parsing weekly routine: %s", err)
                continue

        return weekly

    def _parse_tasks_from_description(self, description: str) -> list[dict[str, Any]]:
        """Parse tasks from event description (YAML or simple list)."""
        tasks = []

        try:
            # Try parsing as YAML
            if "tasks:" in description:
                data = yaml.safe_load(description)
                if isinstance(data, dict) and "tasks" in data:
                    for task in data["tasks"]:
                        if isinstance(task, dict):
                            tasks.append({
                                "title": task.get("title", "Task"),
                                "image": task.get("image"),
                                "duration": task.get("duration", 5),
                                "completed": False,
                            })
                        elif isinstance(task, str):
                            tasks.append({
                                "title": task,
                                "image": None,
                                "duration": 5,
                                "completed": False,
                            })
            else:
                # Parse as simple list (lines starting with - or numbers)
                lines = description.strip().split("\n")
                for line in lines:
                    line = line.strip()
                    if line.startswith("-") or line[0].isdigit():
                        title = line.lstrip("-0123456789.").strip()
                        if title:
                            tasks.append({
                                "title": title,
                                "image": None,
                                "duration": 5,
                                "completed": False,
                            })

        except Exception as err:
            _LOGGER.warning("Error parsing tasks from description: %s", err)

        return tasks

    def _generate_routine_id(self, event: dict) -> str:
        """Generate a unique routine ID from event data."""
        start = event.get("start", "")
        summary = event.get("summary", "")
        return f"{start}_{summary}".replace(" ", "_").replace(":", "")

    def _get_current_routine(
        self, routines: dict[str, dict], now: datetime
    ) -> dict[str, Any] | None:
        """Get the currently active routine."""
        for routine in routines.values():
            if routine["is_current"]:
                return routine
        return None

    def _get_next_routine(
        self, routines: dict[str, dict], now: datetime
    ) -> dict[str, Any] | None:
        """Get the next upcoming routine."""
        future_routines = [
            r for r in routines.values() if r["start_time"] > now
        ]
        if future_routines:
            return min(future_routines, key=lambda r: r["start_time"])
        return None

    async def async_check_task(self, routine_id: str, task_index: int) -> None:
        """Mark a task as complete."""
        if routine_id not in self.data["daily"]:
            raise ValueError(f"Routine {routine_id} not found")

        routine = self.data["daily"][routine_id]
        if task_index < 0 or task_index >= len(routine["tasks"]):
            raise ValueError(f"Task index {task_index} out of range")

        routine["tasks"][task_index]["completed"] = True
        routine["completed_count"] = sum(1 for t in routine["tasks"] if t["completed"])

        # Update state storage
        if routine_id not in self._state:
            self._state[routine_id] = {"tasks": []}

        while len(self._state[routine_id]["tasks"]) <= task_index:
            self._state[routine_id]["tasks"].append({"completed": False})

        self._state[routine_id]["tasks"][task_index]["completed"] = True

        await self._save_state()
        await self.async_request_refresh()

    async def async_uncheck_task(self, routine_id: str, task_index: int) -> None:
        """Mark a task as incomplete."""
        if routine_id not in self.data["daily"]:
            raise ValueError(f"Routine {routine_id} not found")

        routine = self.data["daily"][routine_id]
        if task_index < 0 or task_index >= len(routine["tasks"]):
            raise ValueError(f"Task index {task_index} out of range")

        routine["tasks"][task_index]["completed"] = False
        routine["completed_count"] = sum(1 for t in routine["tasks"] if t["completed"])

        # Update state storage
        if routine_id in self._state and task_index < len(self._state[routine_id]["tasks"]):
            self._state[routine_id]["tasks"][task_index]["completed"] = False

        await self._save_state()
        await self.async_request_refresh()

    async def async_reset_routine(self, routine_id: str) -> None:
        """Reset all tasks in a routine."""
        if routine_id not in self.data["daily"]:
            raise ValueError(f"Routine {routine_id} not found")

        routine = self.data["daily"][routine_id]
        for task in routine["tasks"]:
            task["completed"] = False

        routine["completed_count"] = 0

        # Clear state storage
        if routine_id in self._state:
            del self._state[routine_id]

        await self._save_state()
        await self.async_request_refresh()

    async def async_reset_all(self) -> None:
        """Reset all routines."""
        self._state = {}
        await self._save_state()
        await self.async_request_refresh()

    async def _save_state(self) -> None:
        """Save state to storage."""
        await self._store.async_save({"routines": self._state})
