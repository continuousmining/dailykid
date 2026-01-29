"""Constants for Kids Schedule integration."""
from typing import Final

DOMAIN: Final = "kids_schedule"
NAME: Final = "Kids Schedule"
VERSION: Final = "1.0.0"

# Configuration
CONF_CALENDAR_ENTITY: Final = "calendar_entity"
CONF_ALEXA_ENTITY: Final = "alexa_entity"
CONF_ANNOUNCEMENT_ENABLED: Final = "announcement_enabled"
CONF_TASK_COMPLETE_ANNOUNCEMENT: Final = "task_complete_announcement"
CONF_ROUTINE_START_ANNOUNCEMENT: Final = "routine_start_announcement"
CONF_ROUTINE_COMPLETE_ANNOUNCEMENT: Final = "routine_complete_announcement"
CONF_RESET_TIME: Final = "reset_time"
CONF_REQUIRE_ORDER: Final = "require_order"

# Defaults
DEFAULT_RESET_TIME: Final = "00:00:00"
DEFAULT_REQUIRE_ORDER: Final = False
DEFAULT_ANNOUNCEMENT_ENABLED: Final = True
DEFAULT_TASK_COMPLETE: Final = True
DEFAULT_ROUTINE_START: Final = True
DEFAULT_ROUTINE_COMPLETE: Final = True

# Services
SERVICE_CHECK_TASK: Final = "check_task"
SERVICE_UNCHECK_TASK: Final = "uncheck_task"
SERVICE_RESET_ROUTINE: Final = "reset_routine"
SERVICE_ANNOUNCE: Final = "announce"

# Attributes
ATTR_ROUTINE_ID: Final = "routine_id"
ATTR_TASK_INDEX: Final = "task_index"
ATTR_MESSAGE: Final = "message"
ATTR_TASKS: Final = "tasks"
ATTR_COMPLETED_TASKS: Final = "completed_tasks"
ATTR_TOTAL_TASKS: Final = "total_tasks"
ATTR_PROGRESS: Final = "progress"
ATTR_CURRENT_TASK: Final = "current_task"
ATTR_NEXT_ROUTINE: Final = "next_routine"
ATTR_START_TIME: Final = "start_time"
ATTR_END_TIME: Final = "end_time"
ATTR_IMAGE: Final = "image"
ATTR_DURATION: Final = "duration"
ATTR_IS_CURRENT: Final = "is_current"

# Event types
EVENT_ROUTINE_STARTED: Final = "kids_schedule_routine_started"
EVENT_TASK_COMPLETED: Final = "kids_schedule_task_completed"
EVENT_ROUTINE_COMPLETED: Final = "kids_schedule_routine_completed"

# Storage
STORAGE_KEY: Final = "kids_schedule_state"
STORAGE_VERSION: Final = 1
