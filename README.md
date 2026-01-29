# Kids Schedule for Home Assistant

A child-friendly schedule integration for Home Assistant that displays daily routines with visual task tracking, progress indicators, and Alexa voice announcements.

## Features

✨ **Three View Modes**
- **Daily View**: See today's routines at a glance with progress tracking
- **Weekly View**: Browse 7 days of scheduled routines
- **Full Routine View**: Large, kid-friendly task cards with images and checkboxes

🎯 **Task Management**
- Interactive checkboxes for completing tasks
- Visual progress indicators
- Support for task images (local or URL)
- Task duration tracking
- Optional ordered task completion

🔊 **Alexa Integration**
- Automatic announcements when routines start
- Task completion celebrations
- Routine completion notifications
- Configurable announcement preferences

📅 **Calendar Integration**
- Pulls from any Home Assistant calendar
- Supports both YAML and simple list formats
- Automatic daily reset
- Weekly schedule overview

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/kids_schedule` folder to your Home Assistant's `custom_components` directory
2. Copy the `www/kids-schedule-card` folder to your Home Assistant's `www` directory
3. Restart Home Assistant

## Configuration

### 1. Set Up the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Kids Schedule"
4. Configure:
   - **Name**: Display name for the integration
   - **Calendar Entity**: Select your calendar (e.g., `calendar.family_schedule`)
   - **Alexa Entity** (optional): Select your Alexa media player
   - **Enable Announcements**: Toggle voice announcements on/off
   - **Routine Start Announcements**: Announce when routines begin
   - **Task Complete Announcements**: Celebrate task completion
   - **Routine Complete Announcements**: Celebrate when all tasks are done
   - **Reset Time**: When to reset daily routines (default: midnight)
   - **Require Order**: Force tasks to be completed in order

### 2. Add the Lovelace Card

#### Using UI

1. Edit your dashboard
2. Click "Add Card"
3. Search for "Custom: Kids Schedule Card"
4. Configure the card options

#### Using YAML

```yaml
type: custom:kids-schedule-card
entity: sensor.kids_schedule_daily
title: My Schedule
show_progress: true
show_images: true
show_time: true
```

**Card Configuration Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `entity` | string | **Required** | The daily schedule sensor entity |
| `title` | string | "My Schedule" | Card title |
| `show_progress` | boolean | true | Show progress bars |
| `show_images` | boolean | true | Display task images |
| `show_time` | boolean | true | Show routine start/end times |

### 3. Add the Card Resource

**Important**: You must add the JavaScript file as a resource for the card to work.

#### Via UI:
1. Go to **Settings** → **Dashboards** → **Resources**
2. Click **Add Resource**
3. Enter URL: `/local/kids-schedule-card/kids-schedule-card.js`
4. Select type: **JavaScript Module**
5. Click **Create**

#### Via YAML (configuration.yaml):
```yaml
lovelace:
  mode: yaml
  resources:
    - url: /local/kids-schedule-card/kids-schedule-card.js
      type: module
```

## Calendar Event Format

### YAML Format (Recommended)

Create calendar events with routines defined in YAML format in the event description:

**Event Title:** Morning Routine  
**Start Time:** 7:30 AM  
**End Time:** 8:30 AM  
**Description:**
```yaml
tasks:
  - title: Brush teeth
    image: /local/images/brush-teeth.png
    duration: 5
  - title: Get dressed
    image: https://example.com/images/get-dressed.jpg
    duration: 10
  - title: Eat breakfast
    image: /local/images/breakfast.png
    duration: 15
  - title: Pack backpack
    image: /local/images/backpack.png
    duration: 5
```

### Simple List Format

You can also use a simple list format (lines starting with `-` or numbers):

**Description:**
```
- Brush teeth
- Get dressed
- Eat breakfast
- Pack backpack
```

## Working with Images

### Image Requirements

- **Recommended size**: 512x512 pixels or larger
- **Aspect ratio**: Square (1:1) works best
- **Formats**: PNG, JPG, WEBP, GIF
- **File size**: Keep under 1MB for best performance

### Uploading Images to Home Assistant

#### Option 1: Using File Editor

1. Install the **File Editor** add-on from the Add-on Store
2. Navigate to `/config/www/images/`
3. Create the `images` folder if it doesn't exist
4. Upload your images
5. Reference them as: `/local/images/filename.png`

#### Option 2: Using Samba/FTP

1. Enable Samba Share or SSH access
2. Navigate to `/config/www/images/`
3. Copy your image files
4. Reference them as: `/local/images/filename.png`

#### Option 3: Direct File Access

1. Connect to Home Assistant via SSH or terminal
2. Create directory: `mkdir -p /config/www/images`
3. Copy images to this folder
4. Reference as: `/local/images/filename.png`

### Using External URLs

You can reference images from external URLs:

```yaml
image: https://example.com/images/task-icon.png
```

**Note**: Ensure the URL is publicly accessible and doesn't require authentication.

### Sample Images Directory Structure

```
/config/www/
└── images/
    ├── brush-teeth.png
    ├── get-dressed.png
    ├── breakfast.png
    ├── backpack.png
    ├── homework.png
    ├── dinner.png
    └── bedtime.png
```

### Finding Icons and Images

**Free Image Resources:**
- [Flaticon](https://www.flaticon.com/) - Free icons (attribution required for free tier)
- [Icons8](https://icons8.com/) - Free icons and illustrations
- [Freepik](https://www.freepik.com/) - Free vectors and images
- [Unsplash](https://unsplash.com/) - Free stock photos
- [Material Design Icons](https://pictogrammers.com/library/mdi/) - Icon set used by Home Assistant

**Creating Your Own:**
- Use Canva (free tier available)
- Use GIMP (free image editor)
- Take photos and crop them to square
- Use smartphone drawing apps

## Example Calendar Events

### Complete Morning Routine

```yaml
Title: Morning Routine
Start: 7:00 AM
End: 8:00 AM
Description:
tasks:
  - title: Wake up and stretch
    image: /local/images/wake-up.png
    duration: 5
  - title: Brush teeth
    image: /local/images/brush-teeth.png
    duration: 5
  - title: Wash face
    image: /local/images/wash-face.png
    duration: 3
  - title: Get dressed
    image: /local/images/get-dressed.png
    duration: 10
  - title: Make bed
    image: /local/images/make-bed.png
    duration: 5
  - title: Eat breakfast
    image: /local/images/breakfast.png
    duration: 20
  - title: Pack backpack
    image: /local/images/backpack.png
    duration: 5
  - title: Put on shoes
    image: /local/images/shoes.png
    duration: 3
```

### After School Routine

```yaml
Title: After School
Start: 3:30 PM
End: 5:00 PM
Description:
tasks:
  - title: Put away backpack
    image: /local/images/backpack-away.png
    duration: 2
  - title: Wash hands
    image: /local/images/wash-hands.png
    duration: 3
  - title: Have a snack
    image: /local/images/snack.png
    duration: 15
  - title: Do homework
    image: /local/images/homework.png
    duration: 45
  - title: Free play time
    image: /local/images/play.png
    duration: 30
```

### Bedtime Routine

```yaml
Title: Bedtime Routine
Start: 8:00 PM
End: 9:00 PM
Description:
tasks:
  - title: Put away toys
    image: /local/images/cleanup.png
    duration: 10
  - title: Take a bath
    image: /local/images/bath.png
    duration: 20
  - title: Brush teeth
    image: /local/images/brush-teeth.png
    duration: 5
  - title: Put on pajamas
    image: /local/images/pajamas.png
    duration: 5
  - title: Read a story
    image: /local/images/book.png
    duration: 15
  - title: Lights out
    image: /local/images/sleep.png
    duration: 5
```

## Alexa Announcements Setup

### Prerequisites

You need one of the following:
- **Alexa Media Player** custom integration (recommended)
- **Nabu Casa** with Alexa integration
- Standard Home Assistant Alexa integration

### Install Alexa Media Player (Recommended)

1. Install via HACS:
   - Go to HACS → Integrations
   - Search for "Alexa Media Player"
   - Install and restart Home Assistant

2. Configure:
   - Go to Settings → Integrations → Add Integration
   - Search for "Alexa Media Player"
   - Follow authentication steps
   - Your Alexa devices will appear as `media_player.echo_*`

3. Select device in Kids Schedule config:
   - Choose your preferred Alexa device
   - Enable announcements

### Announcement Examples

When enabled, you'll hear:

**Routine Start:**
> "It's time for morning routine! First, brush your teeth."

**Task Complete:**
> "Nice work! 3 of 5 tasks done."

**Routine Complete:**
> "Great job! You finished morning routine!"

### Customizing Announcements

You can create custom automations for more control:

```yaml
automation:
  - alias: "Custom Routine Start"
    trigger:
      - platform: event
        event_type: kids_schedule_routine_started
    action:
      - service: notify.alexa_media_echo_dot
        data:
          message: "Time to start {{ trigger.event.data.routine_title }}! You've got this!"
          data:
            type: announce
```

## Services

The integration provides these services for automation:

### kids_schedule.check_task

Mark a task as completed.

```yaml
service: kids_schedule.check_task
data:
  routine_id: "2025-01-28T07:00:00Z_Morning_Routine"
  task_index: 0
```

### kids_schedule.uncheck_task

Mark a task as incomplete.

```yaml
service: kids_schedule.uncheck_task
data:
  routine_id: "2025-01-28T07:00:00Z_Morning_Routine"
  task_index: 0
```

### kids_schedule.reset_routine

Reset all tasks in a routine.

```yaml
service: kids_schedule.reset_routine
data:
  routine_id: "2025-01-28T07:00:00Z_Morning_Routine"
```

### kids_schedule.announce

Send a custom announcement.

```yaml
service: kids_schedule.announce
data:
  message: "Great job finishing your homework!"
```

## Automation Examples

### Announce Routine Start with Lights

```yaml
automation:
  - alias: "Morning Routine - Lights and Announcement"
    trigger:
      - platform: time
        at: "07:00:00"
    condition:
      - condition: state
        entity_id: binary_sensor.workday_sensor
        state: "on"
    action:
      - service: light.turn_on
        target:
          entity_id: light.kids_bedroom
        data:
          brightness_pct: 50
      - service: kids_schedule.announce
        data:
          message: "Good morning! Time to start your morning routine!"
```

### Reward System for Completed Routines

```yaml
automation:
  - alias: "Routine Complete - Reward Star"
    trigger:
      - platform: event
        event_type: kids_schedule_routine_completed
    action:
      - service: counter.increment
        target:
          entity_id: counter.completed_routines
      - service: kids_schedule.announce
        data:
          message: "You earned a gold star! That's {{ states('counter.completed_routines') }} stars this week!"
```

### Weekend Schedule Adjustment

```yaml
automation:
  - alias: "Weekend Morning - Later Start"
    trigger:
      - platform: time
        at: "09:00:00"
    condition:
      - condition: state
        entity_id: binary_sensor.workday_sensor
        state: "off"
    action:
      - service: kids_schedule.announce
        data:
          message: "Good morning! It's the weekend, so you can take your time with your routine today!"
```

## Troubleshooting

### Card Not Showing

1. Verify the resource is added:
   - Settings → Dashboards → Resources
   - Look for `/local/kids-schedule-card/kids-schedule-card.js`

2. Clear browser cache:
   - Press `Ctrl + Shift + R` (or `Cmd + Shift + R` on Mac)

3. Check browser console for errors:
   - Press `F12` to open developer tools
   - Look for error messages

### Images Not Loading

1. Check file path:
   - `/local/` maps to `/config/www/`
   - Ensure files are in `/config/www/images/`

2. Check file permissions:
   ```bash
   chmod 644 /config/www/images/*
   ```

3. Verify image URLs:
   - Test external URLs in browser first
   - Ensure URLs are publicly accessible

### Calendar Events Not Showing

1. Verify calendar entity exists:
   - Developer Tools → States
   - Search for your calendar entity

2. Check event format:
   - Ensure YAML is properly indented
   - Use YAML validators if needed

3. Review logs:
   - Settings → System → Logs
   - Search for "kids_schedule"

### Alexa Not Announcing

1. Verify Alexa entity is configured:
   - Settings → Devices & Services → Kids Schedule
   - Check Alexa entity is selected

2. Test announcement manually:
   ```yaml
   service: kids_schedule.announce
   data:
     message: "Test announcement"
   ```

3. Check Alexa Media Player status:
   - Ensure device is online
   - Verify "Do Not Disturb" is off

## Support

For issues, feature requests, or questions:
- GitHub Issues: [Create an issue]
- Home Assistant Community: [Community Forum Thread]

## Credits

Developed by Jason for MSP automation and home assistant enthusiasts.

## License

MIT License - see LICENSE file for details
