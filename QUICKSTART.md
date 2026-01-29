# Quick Start Guide - Kids Schedule

This guide will get you up and running with Kids Schedule in under 10 minutes!

## Step 1: Install the Integration (5 minutes)

### Via HACS (Recommended)
1. Open **HACS** → **Integrations**
2. Click **⋮** (three dots) → **Custom repositories**
3. Add repository URL: `https://github.com/yourusername/kids-schedule`
4. Category: **Integration**
5. Click **Install**
6. **Restart Home Assistant**

### Manual Install
1. Copy `custom_components/kids_schedule` to your HA config
2. Copy `www/kids-schedule-card` to your HA www folder
3. Restart Home Assistant

## Step 2: Add the JavaScript Resource (1 minute)

**Important!** The card won't work without this step.

1. Go to **Settings** → **Dashboards** → **Resources**
2. Click **Add Resource**
3. URL: `/local/kids-schedule-card/kids-schedule-card.js`
4. Type: **JavaScript Module**
5. Click **Create**

## Step 3: Configure the Integration (2 minutes)

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Kids Schedule"
4. Fill in:
   - **Name**: Kids Schedule (or your child's name)
   - **Calendar**: Select your calendar entity
   - **Alexa Device** (optional): Select if you want voice announcements
   - Leave other settings as default for now
5. Click **Submit**

## Step 4: Create Your First Calendar Event (2 minutes)

Open your calendar (Google Calendar, CalDAV, etc.) and create a test event:

**Title:** Morning Routine  
**Date:** Today  
**Time:** 7:00 AM - 8:00 AM  
**Description:**
```yaml
tasks:
  - title: Brush teeth
    duration: 5
  - title: Get dressed
    duration: 10
  - title: Eat breakfast
    duration: 15
```

Save the event. Home Assistant will pick it up within a minute.

## Step 5: Add the Card to Your Dashboard (2 minutes)

1. Edit your dashboard
2. Click **Add Card**
3. Scroll down and select **Custom: Kids Schedule Card**
4. Configure:
   - **Entity**: `sensor.kids_schedule_daily`
   - **Title**: My Schedule (or your child's name)
5. Click **Save**

## You're Done! 🎉

You should now see your routine card with the morning routine!

---

## Next Steps

### Add Images to Tasks

Images make tasks more engaging for kids!

**Quick Method:**
1. Go to **Settings** → **Add-ons**
2. Install **File Editor**
3. Open File Editor
4. Navigate to `/config/www/` and create an `images` folder
5. Upload images (512x512 PNG works great)
6. Update your calendar event:
   ```yaml
   tasks:
     - title: Brush teeth
       image: /local/images/brush-teeth.png
       duration: 5
   ```

**Free Image Resources:**
- [Flaticon](https://www.flaticon.com/) - Tons of free icons
- [Icons8](https://icons8.com/) - Great for kid-friendly graphics

### Enable Alexa Announcements

If you have Alexa:

1. Install **Alexa Media Player** via HACS
2. Configure it with your Amazon account
3. Go to **Settings** → **Devices & Services** → **Kids Schedule**
4. Click **Configure**
5. Select your Alexa device
6. Enable announcement options

Now Alexa will announce when routines start and celebrate task completion!

### Create More Routines

Add these common routines:

**After School Routine** (3:30 PM - 5:00 PM)
```yaml
tasks:
  - title: Put away backpack
    duration: 2
  - title: Wash hands
    duration: 3
  - title: Have a snack
    duration: 15
  - title: Do homework
    duration: 45
```

**Bedtime Routine** (8:00 PM - 9:00 PM)
```yaml
tasks:
  - title: Put away toys
    duration: 10
  - title: Take a bath
    duration: 20
  - title: Brush teeth
    duration: 5
  - title: Read a story
    duration: 15
```

### Add Reward System

Create a star counter for motivation:

**configuration.yaml:**
```yaml
counter:
  routine_stars:
    name: Weekly Stars
    icon: mdi:star
```

**automation:**
```yaml
- alias: "Reward Star on Completion"
  trigger:
    - platform: event
      event_type: kids_schedule_routine_completed
  action:
    - service: counter.increment
      target:
        entity_id: counter.routine_stars
    - service: kids_schedule.announce
      data:
        message: "You earned a star! That's {{ states('counter.routine_stars') }} stars this week!"
```

---

## Common Issues

### "Entity not found" error
- Wait 1 minute for the integration to poll the calendar
- Check that your calendar has events scheduled
- Restart Home Assistant

### Card not showing
- Verify you added the JavaScript resource (Step 2)
- Clear browser cache: Ctrl+Shift+R (Cmd+Shift+R on Mac)
- Check browser console (F12) for errors

### Images not loading
- Images must be in `/config/www/images/`
- Path must start with `/local/`
- Example: `/local/images/brush-teeth.png`

### Calendar events not appearing
- Ensure event format is correct (YAML must be indented properly)
- Check that event is scheduled for today
- View Developer Tools → States → search for your calendar entity

---

## Tips for Success

✅ **Start Simple**: Begin with 3-4 tasks per routine  
✅ **Use Images**: Kids respond much better to visual cues  
✅ **Consistent Times**: Keep routine times consistent daily  
✅ **Celebrate Success**: Use announcements and rewards  
✅ **Involve Your Kids**: Let them help choose images and tasks  
✅ **Be Flexible**: Adjust times and tasks based on what works  

---

## Getting Help

- **Full Documentation**: See README.md
- **Example Automations**: See example_automations.yaml
- **Issues**: [GitHub Issues](https://github.com/yourusername/kids-schedule/issues)
- **Community**: [Home Assistant Forum](https://community.home-assistant.io/)

Enjoy helping your kids build better routines! 🌟
