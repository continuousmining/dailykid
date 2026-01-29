# Kids Schedule Integration for Home Assistant

Transform your child's daily routines into an engaging, interactive experience with visual task tracking, progress monitoring, and voice announcements!

## 🌟 Key Features

### 📱 Three Interactive Views
- **Daily View** - Today's routines with progress bars and task previews
- **Weekly View** - 7-day schedule overview
- **Full Routine View** - Large, kid-friendly task cards with checkboxes

### ✅ Task Management
- Interactive checkboxes kids can tap themselves
- Visual progress indicators (progress bars & completion percentages)
- Support for task images (upload your own or use URLs)
- Task duration tracking
- Optional: require tasks to be completed in order

### 🔊 Alexa Voice Integration
- Automatic announcements when routines start
- Celebrations when tasks are completed
- Special announcement when full routine is done
- Fully configurable announcement preferences

### 📅 Calendar-Based
- Works with any Home Assistant calendar
- Simple YAML or list format in event descriptions
- Automatic daily reset at midnight (or custom time)
- Weekly schedule overview

### 🎨 Beautiful, Kid-Friendly UI
- Colorful, engaging design
- Large touch-friendly buttons perfect for tablets
- Smooth animations and transitions
- Progress celebrations with icons and colors

## 📸 Screenshots

### Daily View
See all of today's routines at a glance with progress tracking and quick task previews.

### Routine Detail View
Large, colorful task cards with images make it easy for kids to know what to do next.

### Weekly Overview
Browse the entire week's schedule to help kids prepare for upcoming routines.

## 🚀 Quick Start

1. **Install via HACS** (or manually copy files)
2. **Add JavaScript resource** to Dashboards → Resources
3. **Configure** the integration with your calendar
4. **Create calendar events** with task lists
5. **Add the card** to your dashboard
6. **Upload task images** to `/config/www/images/` (optional)

Full setup takes less than 10 minutes! See [QUICKSTART.md](QUICKSTART.md) for step-by-step instructions.

## 📋 Example Calendar Event

```yaml
Title: Morning Routine
Time: 7:00 AM - 8:00 AM
Description:
tasks:
  - title: Brush teeth
    image: /local/images/brush-teeth.png
    duration: 5
  - title: Get dressed
    image: /local/images/get-dressed.png
    duration: 10
  - title: Eat breakfast
    image: /local/images/breakfast.png
    duration: 15
  - title: Pack backpack
    image: /local/images/backpack.png
    duration: 5
```

## 🎯 Perfect For

- **Parents** wanting to build better routines for their kids
- **Teachers** using Home Assistant in classrooms
- **Special needs** children who benefit from visual schedules
- **Families** wanting to gamify chores and responsibilities
- **Anyone** looking to add structure to their child's day

## 🛠️ Integrations

Works seamlessly with:
- ✅ Google Calendar
- ✅ Local Calendar
- ✅ CalDAV calendars
- ✅ Office 365 Calendar
- ✅ Alexa Media Player (for announcements)
- ✅ Any HA calendar entity

## 📚 Documentation

- [README.md](README.md) - Complete documentation
- [QUICKSTART.md](QUICKSTART.md) - 10-minute setup guide
- [IMAGES.md](IMAGES.md) - How to create/find task images
- [example_automations.yaml](example_automations.yaml) - Sample automations

## 🎁 Bonus Features

- **Reward system** - Track stars/points for completed routines
- **Smart notifications** - Remind kids if they haven't started
- **Visual cues** - Change LED colors based on progress
- **Parent notifications** - Get alerts when routines complete
- **Weekend mode** - Different schedules for school vs. weekend days

## 💡 Use Cases

### Morning Routines
Help kids get ready for school independently with a clear checklist of tasks.

### After School
Structure homework time, chores, and playtime with visual task tracking.

### Bedtime Routines
Make bedtime smoother with a consistent, visual routine kids can follow.

### Chore Charts
Turn chores into a game with progress bars and completion celebrations.

### Special Needs
Provide structure and predictability for children who thrive on routine.

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/kids-schedule/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/kids-schedule/discussions)
- **Community**: [Home Assistant Forum](https://community.home-assistant.io/)

## ⭐ Credits

Created for parents who want to help their kids build better habits through technology!

## 📄 License

MIT License - See [LICENSE](LICENSE) for details
