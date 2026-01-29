"""Sensor platform for Kids Schedule."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ATTR_TASKS, ATTR_COMPLETED_TASKS, ATTR_TOTAL_TASKS, ATTR_PROGRESS
from .coordinator import KidsScheduleCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Kids Schedule sensor from a config entry."""
    coordinator: KidsScheduleCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = [
        KidsScheduleDailySensor(coordinator, config_entry),
        KidsScheduleWeeklySensor(coordinator, config_entry),
        KidsScheduleCurrentRoutineSensor(coordinator, config_entry),
    ]

    async_add_entities(sensors)


class KidsScheduleDailySensor(CoordinatorEntity, SensorEntity):
    """Sensor for daily schedule."""

    def __init__(
        self, coordinator: KidsScheduleCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = f"{config_entry.title} Daily"
        self._attr_unique_id = f"{config_entry.entry_id}_daily"
        self._attr_icon = "mdi:calendar-today"

    @property
    def native_value(self) -> int:
        """Return the number of routines today."""
        return len(self.coordinator.data.get("daily", {}))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        daily_data = self.coordinator.data.get("daily", {})
        
        routines_list = []
        for routine in daily_data.values():
            routines_list.append({
                "id": routine["id"],
                "title": routine["title"],
                "start_time": routine["start_time"].isoformat(),
                "end_time": routine["end_time"].isoformat(),
                "is_current": routine["is_current"],
                "completed": routine["completed_count"],
                "total": routine["total_count"],
                "progress": (
                    round((routine["completed_count"] / routine["total_count"]) * 100)
                    if routine["total_count"] > 0
                    else 0
                ),
                "tasks": routine["tasks"],
            })

        # Sort by start time
        routines_list.sort(key=lambda r: r["start_time"])

        return {
            "routines": routines_list,
            "current_routine": self.coordinator.data.get("current_routine"),
            "next_routine": self.coordinator.data.get("next_routine"),
        }


class KidsScheduleWeeklySensor(CoordinatorEntity, SensorEntity):
    """Sensor for weekly schedule."""

    def __init__(
        self, coordinator: KidsScheduleCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = f"{config_entry.title} Weekly"
        self._attr_unique_id = f"{config_entry.entry_id}_weekly"
        self._attr_icon = "mdi:calendar-week"

    @property
    def native_value(self) -> int:
        """Return the total number of routines this week."""
        weekly_data = self.coordinator.data.get("weekly", {})
        return sum(len(routines) for routines in weekly_data.values())

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        weekly_data = self.coordinator.data.get("weekly", {})
        
        # Format for frontend
        weekly_formatted = {}
        for day, routines in weekly_data.items():
            weekly_formatted[day] = [
                {
                    "id": r["id"],
                    "title": r["title"],
                    "start_time": r["start_time"].isoformat(),
                    "end_time": r["end_time"].isoformat(),
                    "task_count": r["task_count"],
                }
                for r in routines
            ]

        return {"weekly_schedule": weekly_formatted}


class KidsScheduleCurrentRoutineSensor(CoordinatorEntity, SensorEntity):
    """Sensor for the current active routine."""

    def __init__(
        self, coordinator: KidsScheduleCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = f"{config_entry.title} Current Routine"
        self._attr_unique_id = f"{config_entry.entry_id}_current"
        self._attr_icon = "mdi:clock-outline"

    @property
    def native_value(self) -> str:
        """Return the current routine name."""
        current = self.coordinator.data.get("current_routine")
        if current:
            return current["title"]
        return "None"

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        current = self.coordinator.data.get("current_routine")
        
        if not current:
            next_routine = self.coordinator.data.get("next_routine")
            if next_routine:
                return {
                    "status": "waiting",
                    "next_routine": next_routine["title"],
                    "next_start": next_routine["start_time"].isoformat(),
                }
            return {"status": "none"}

        return {
            "status": "active",
            "id": current["id"],
            "title": current["title"],
            "start_time": current["start_time"].isoformat(),
            "end_time": current["end_time"].isoformat(),
            "completed": current["completed_count"],
            "total": current["total_count"],
            "progress": (
                round((current["completed_count"] / current["total_count"]) * 100)
                if current["total_count"] > 0
                else 0
            ),
            "tasks": current["tasks"],
            "current_task": self._get_current_task(current),
        }

    def _get_current_task(self, routine: dict[str, Any]) -> dict[str, Any] | None:
        """Get the current task to work on."""
        require_order = self._config_entry.data.get("require_order", False)

        if require_order:
            # Return first incomplete task
            for i, task in enumerate(routine["tasks"]):
                if not task["completed"]:
                    return {
                        "index": i,
                        "title": task["title"],
                        "image": task.get("image"),
                        "duration": task.get("duration", 5),
                    }
        else:
            # Return any incomplete task (first one found)
            for i, task in enumerate(routine["tasks"]):
                if not task["completed"]:
                    return {
                        "index": i,
                        "title": task["title"],
                        "image": task.get("image"),
                        "duration": task.get("duration", 5),
                    }

        return None
