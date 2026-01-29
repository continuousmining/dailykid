/**
 * Kids Schedule Card
 * Custom Lovelace card for displaying child-friendly daily routines
 */

class KidsScheduleCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._config = {};
    this._hass = {};
    this._view = 'daily'; // daily, weekly, or routine
    this._selectedRoutine = null;
    this._selectedDay = null;
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('Please define an entity');
    }
    this._config = {
      entity: config.entity,
      title: config.title || 'My Schedule',
      show_progress: config.show_progress !== false,
      show_images: config.show_images !== false,
      show_time: config.show_time !== false,
      theme: config.theme || 'default',
      ...config,
    };
    this.render();
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  getCardSize() {
    return 6;
  }

  render() {
    if (!this._config.entity) return;

    const entity = this._hass.states[this._config.entity];
    if (!entity) {
      this.shadowRoot.innerHTML = '<ha-card>Entity not found</ha-card>';
      return;
    }

    const routines = entity.attributes.routines || [];
    const currentRoutine = entity.attributes.current_routine;
    const nextRoutine = entity.attributes.next_routine;

    // Get weekly entity for weekly view
    const weeklyEntityId = this._config.entity.replace('_daily', '_weekly');
    const weeklyEntity = this._hass.states[weeklyEntityId];
    const weeklySchedule = weeklyEntity?.attributes.weekly_schedule || {};

    this.shadowRoot.innerHTML = `
      ${this.getStyles()}
      <ha-card>
        <div class="card-content">
          ${this.renderHeader()}
          ${this._view === 'daily' ? this.renderDailyView(routines, currentRoutine, nextRoutine) : ''}
          ${this._view === 'weekly' ? this.renderWeeklyView(weeklySchedule) : ''}
          ${this._view === 'routine' ? this.renderRoutineView(this._selectedRoutine) : ''}
        </div>
      </ha-card>
    `;

    this.attachEventListeners();
  }

  renderHeader() {
    const backButton = this._view !== 'daily' ? `
      <button class="back-button" data-action="back">
        <ha-icon icon="mdi:arrow-left"></ha-icon>
      </button>
    ` : '';

    const viewToggle = this._view === 'daily' ? `
      <button class="view-toggle" data-action="toggle-weekly">
        <ha-icon icon="mdi:calendar-week"></ha-icon>
      </button>
    ` : '';

    return `
      <div class="header">
        ${backButton}
        <h2 class="title">${this.getTitle()}</h2>
        ${viewToggle}
      </div>
    `;
  }

  getTitle() {
    if (this._view === 'routine' && this._selectedRoutine) {
      return this._selectedRoutine.title;
    }
    if (this._view === 'weekly') {
      return 'This Week';
    }
    return this._config.title;
  }

  renderDailyView(routines, currentRoutine, nextRoutine) {
    if (!routines || routines.length === 0) {
      return `
        <div class="empty-state">
          <ha-icon icon="mdi:calendar-blank"></ha-icon>
          <p>No routines scheduled for today</p>
        </div>
      `;
    }

    const routineCards = routines.map(routine => {
      const isCurrent = routine.is_current;
      const isComplete = routine.completed === routine.total;
      const progressPercent = (routine.completed / routine.total) * 100;

      return `
        <div class="routine-card ${isCurrent ? 'current' : ''} ${isComplete ? 'complete' : ''}" 
             data-routine-id="${routine.id}">
          <div class="routine-header">
            <div class="routine-info">
              <h3 class="routine-title">${routine.title}</h3>
              ${this._config.show_time ? `
                <span class="routine-time">
                  ${this.formatTime(routine.start_time)} - ${this.formatTime(routine.end_time)}
                </span>
              ` : ''}
            </div>
            ${isCurrent ? '<span class="badge current-badge">Now</span>' : ''}
            ${isComplete ? '<span class="badge complete-badge">Done!</span>' : ''}
          </div>
          
          ${this._config.show_progress ? `
            <div class="progress-bar">
              <div class="progress-fill" style="width: ${progressPercent}%"></div>
            </div>
            <div class="progress-text">${routine.completed} of ${routine.total} tasks</div>
          ` : ''}

          <div class="task-preview">
            ${routine.tasks.slice(0, 3).map((task, index) => `
              <div class="task-preview-item ${task.completed ? 'completed' : ''}">
                <ha-icon icon="${task.completed ? 'mdi:check-circle' : 'mdi:circle-outline'}"></ha-icon>
                <span>${task.title}</span>
              </div>
            `).join('')}
            ${routine.tasks.length > 3 ? `
              <div class="task-preview-more">+${routine.tasks.length - 3} more</div>
            ` : ''}
          </div>

          <button class="open-routine-btn" data-routine-id="${routine.id}">
            <span>Open Routine</span>
            <ha-icon icon="mdi:chevron-right"></ha-icon>
          </button>
        </div>
      `;
    }).join('');

    const nextRoutineCard = nextRoutine && !currentRoutine ? `
      <div class="next-routine-card">
        <ha-icon icon="mdi:clock-outline"></ha-icon>
        <div>
          <p class="next-label">Up Next</p>
          <p class="next-title">${nextRoutine.title}</p>
          <p class="next-time">Starts at ${this.formatTime(nextRoutine.start_time)}</p>
        </div>
      </div>
    ` : '';

    return `
      ${nextRoutineCard}
      <div class="routines-list">
        ${routineCards}
      </div>
    `;
  }

  renderWeeklyView(weeklySchedule) {
    const days = Object.keys(weeklySchedule).sort();
    
    if (days.length === 0) {
      return `
        <div class="empty-state">
          <ha-icon icon="mdi:calendar-blank"></ha-icon>
          <p>No routines scheduled this week</p>
        </div>
      `;
    }

    return `
      <div class="weekly-view">
        ${days.map(day => {
          const date = new Date(day);
          const dayName = date.toLocaleDateString('en-US', { weekday: 'long' });
          const dayDate = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
          const routines = weeklySchedule[day];
          const isToday = day === new Date().toISOString().split('T')[0];

          return `
            <div class="day-card ${isToday ? 'today' : ''}" data-day="${day}">
              <div class="day-header">
                <h3>${dayName}</h3>
                <span class="day-date">${dayDate}</span>
                ${isToday ? '<span class="badge today-badge">Today</span>' : ''}
              </div>
              <div class="day-routines">
                ${routines.map(routine => `
                  <div class="day-routine" data-routine-id="${routine.id}">
                    <span class="routine-time">${this.formatTime(routine.start_time)}</span>
                    <span class="routine-title">${routine.title}</span>
                    <span class="task-count">${routine.task_count} tasks</span>
                  </div>
                `).join('')}
              </div>
            </div>
          `;
        }).join('')}
      </div>
    `;
  }

  renderRoutineView(routine) {
    if (!routine) {
      return '<div class="empty-state"><p>Routine not found</p></div>';
    }

    const progressPercent = (routine.completed / routine.total) * 100;
    const isComplete = routine.completed === routine.total;

    return `
      <div class="routine-detail-view">
        <div class="routine-detail-header">
          ${this._config.show_progress ? `
            <div class="large-progress">
              <svg class="progress-ring" width="120" height="120">
                <circle class="progress-ring-bg" cx="60" cy="60" r="54" />
                <circle class="progress-ring-fill" cx="60" cy="60" r="54" 
                        style="stroke-dashoffset: ${339.292 - (339.292 * progressPercent) / 100}" />
              </svg>
              <div class="progress-center">
                <span class="progress-number">${routine.completed}</span>
                <span class="progress-total">of ${routine.total}</span>
              </div>
            </div>
          ` : ''}
          
          ${isComplete ? `
            <div class="complete-celebration">
              <ha-icon icon="mdi:trophy"></ha-icon>
              <h3>All Done!</h3>
              <p>Great job completing this routine!</p>
            </div>
          ` : ''}
        </div>

        <div class="tasks-list">
          ${routine.tasks.map((task, index) => `
            <div class="task-card ${task.completed ? 'completed' : ''}" 
                 data-task-index="${index}" data-routine-id="${routine.id}">
              <div class="task-checkbox">
                <button class="checkbox-btn" 
                        data-action="toggle-task" 
                        data-routine-id="${routine.id}" 
                        data-task-index="${index}">
                  <ha-icon icon="${task.completed ? 'mdi:checkbox-marked-circle' : 'mdi:checkbox-blank-circle-outline'}"></ha-icon>
                </button>
              </div>
              
              ${this._config.show_images && task.image ? `
                <div class="task-image">
                  <img src="${task.image}" alt="${task.title}" />
                </div>
              ` : ''}
              
              <div class="task-content">
                <h4 class="task-title">${task.title}</h4>
                ${task.duration ? `
                  <span class="task-duration">
                    <ha-icon icon="mdi:clock-outline"></ha-icon>
                    ${task.duration} min
                  </span>
                ` : ''}
              </div>
            </div>
          `).join('')}
        </div>

        <div class="routine-actions">
          <button class="reset-btn" data-action="reset-routine" data-routine-id="${routine.id}">
            <ha-icon icon="mdi:refresh"></ha-icon>
            Reset Routine
          </button>
        </div>
      </div>
    `;
  }

  formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    });
  }

  attachEventListeners() {
    // Back button
    this.shadowRoot.querySelectorAll('[data-action="back"]').forEach(btn => {
      btn.addEventListener('click', () => {
        this._view = this._selectedDay ? 'weekly' : 'daily';
        this._selectedRoutine = null;
        this._selectedDay = null;
        this.render();
      });
    });

    // Toggle weekly view
    this.shadowRoot.querySelectorAll('[data-action="toggle-weekly"]').forEach(btn => {
      btn.addEventListener('click', () => {
        this._view = 'weekly';
        this.render();
      });
    });

    // Open routine from daily view
    this.shadowRoot.querySelectorAll('.open-routine-btn, .routine-card').forEach(card => {
      card.addEventListener('click', (e) => {
        if (e.target.closest('[data-action="toggle-task"]')) return;
        
        const routineId = card.dataset.routineId || card.closest('[data-routine-id]').dataset.routineId;
        const entity = this._hass.states[this._config.entity];
        const routine = entity.attributes.routines.find(r => r.id === routineId);
        
        if (routine) {
          this._selectedRoutine = routine;
          this._view = 'routine';
          this.render();
        }
      });
    });

    // Toggle task
    this.shadowRoot.querySelectorAll('[data-action="toggle-task"]').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.stopPropagation();
        const routineId = btn.dataset.routineId;
        const taskIndex = parseInt(btn.dataset.taskIndex);
        
        const entity = this._hass.states[this._config.entity];
        const routine = entity.attributes.routines.find(r => r.id === routineId);
        const task = routine.tasks[taskIndex];
        
        const service = task.completed ? 'uncheck_task' : 'check_task';
        
        await this._hass.callService('kids_schedule', service, {
          routine_id: routineId,
          task_index: taskIndex,
        });

        // Wait a bit for state update then refresh
        setTimeout(() => {
          const updatedEntity = this._hass.states[this._config.entity];
          const updatedRoutine = updatedEntity.attributes.routines.find(r => r.id === routineId);
          this._selectedRoutine = updatedRoutine;
          this.render();
        }, 500);
      });
    });

    // Reset routine
    this.shadowRoot.querySelectorAll('[data-action="reset-routine"]').forEach(btn => {
      btn.addEventListener('click', async () => {
        const routineId = btn.dataset.routineId;
        
        await this._hass.callService('kids_schedule', 'reset_routine', {
          routine_id: routineId,
        });

        setTimeout(() => {
          const entity = this._hass.states[this._config.entity];
          const routine = entity.attributes.routines.find(r => r.id === routineId);
          this._selectedRoutine = routine;
          this.render();
        }, 500);
      });
    });
  }

  getStyles() {
    return `
      <style>
        :host {
          --primary-color: var(--accent-color, #03a9f4);
          --text-primary: var(--primary-text-color, #212121);
          --text-secondary: var(--secondary-text-color, #727272);
          --card-background: var(--card-background-color, #fff);
          --divider-color: var(--divider-color, #e0e0e0);
          --success-color: #4caf50;
          --warning-color: #ff9800;
        }

        ha-card {
          padding: 16px;
          overflow: hidden;
        }

        .card-content {
          padding: 0;
        }

        .header {
          display: flex;
          align-items: center;
          margin-bottom: 20px;
          gap: 12px;
        }

        .title {
          flex: 1;
          margin: 0;
          font-size: 24px;
          font-weight: bold;
          color: var(--text-primary);
        }

        .back-button, .view-toggle {
          background: var(--divider-color);
          border: none;
          border-radius: 50%;
          width: 40px;
          height: 40px;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: background 0.2s;
        }

        .back-button:hover, .view-toggle:hover {
          background: var(--primary-color);
          color: white;
        }

        .empty-state {
          text-align: center;
          padding: 60px 20px;
          color: var(--text-secondary);
        }

        .empty-state ha-icon {
          font-size: 64px;
          opacity: 0.3;
          margin-bottom: 16px;
        }

        /* Daily View */
        .next-routine-card {
          display: flex;
          align-items: center;
          gap: 16px;
          padding: 16px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-radius: 12px;
          margin-bottom: 20px;
        }

        .next-routine-card ha-icon {
          font-size: 48px;
        }

        .next-label {
          font-size: 12px;
          opacity: 0.9;
          margin: 0 0 4px 0;
        }

        .next-title {
          font-size: 18px;
          font-weight: bold;
          margin: 0 0 4px 0;
        }

        .next-time {
          font-size: 14px;
          margin: 0;
          opacity: 0.9;
        }

        .routines-list {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }

        .routine-card {
          background: var(--card-background);
          border: 2px solid var(--divider-color);
          border-radius: 16px;
          padding: 20px;
          cursor: pointer;
          transition: all 0.3s;
        }

        .routine-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .routine-card.current {
          border-color: var(--primary-color);
          background: linear-gradient(to right, rgba(3, 169, 244, 0.05), transparent);
        }

        .routine-card.complete {
          opacity: 0.7;
          border-color: var(--success-color);
        }

        .routine-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 12px;
        }

        .routine-info {
          flex: 1;
        }

        .routine-title {
          margin: 0 0 4px 0;
          font-size: 20px;
          font-weight: bold;
          color: var(--text-primary);
        }

        .routine-time {
          font-size: 14px;
          color: var(--text-secondary);
        }

        .badge {
          padding: 4px 12px;
          border-radius: 12px;
          font-size: 12px;
          font-weight: bold;
          text-transform: uppercase;
        }

        .current-badge {
          background: var(--primary-color);
          color: white;
        }

        .complete-badge {
          background: var(--success-color);
          color: white;
        }

        .today-badge {
          background: var(--warning-color);
          color: white;
        }

        .progress-bar {
          height: 8px;
          background: var(--divider-color);
          border-radius: 4px;
          overflow: hidden;
          margin: 12px 0;
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, var(--primary-color), var(--success-color));
          transition: width 0.5s ease;
        }

        .progress-text {
          font-size: 14px;
          color: var(--text-secondary);
          margin-bottom: 12px;
        }

        .task-preview {
          margin: 16px 0;
        }

        .task-preview-item {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 8px 0;
          color: var(--text-primary);
        }

        .task-preview-item.completed {
          text-decoration: line-through;
          opacity: 0.6;
        }

        .task-preview-item ha-icon {
          font-size: 20px;
        }

        .task-preview-more {
          padding: 8px 0;
          color: var(--text-secondary);
          font-size: 14px;
          font-style: italic;
        }

        .open-routine-btn {
          display: flex;
          align-items: center;
          justify-content: space-between;
          width: 100%;
          padding: 12px 16px;
          background: var(--primary-color);
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 16px;
          font-weight: bold;
          cursor: pointer;
          margin-top: 12px;
          transition: opacity 0.2s;
        }

        .open-routine-btn:hover {
          opacity: 0.9;
        }

        /* Weekly View */
        .weekly-view {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }

        .day-card {
          background: var(--card-background);
          border: 2px solid var(--divider-color);
          border-radius: 12px;
          padding: 16px;
          transition: all 0.2s;
        }

        .day-card.today {
          border-color: var(--warning-color);
        }

        .day-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 12px;
        }

        .day-header h3 {
          margin: 0;
          font-size: 18px;
          color: var(--text-primary);
        }

        .day-date {
          font-size: 14px;
          color: var(--text-secondary);
        }

        .day-routines {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .day-routine {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 8px 12px;
          background: var(--divider-color);
          border-radius: 8px;
          cursor: pointer;
          transition: background 0.2s;
        }

        .day-routine:hover {
          background: var(--primary-color);
          color: white;
        }

        .day-routine .routine-time {
          font-size: 12px;
          min-width: 60px;
          font-weight: bold;
        }

        .day-routine .routine-title {
          flex: 1;
          font-size: 14px;
        }

        .day-routine .task-count {
          font-size: 12px;
          opacity: 0.7;
        }

        /* Routine Detail View */
        .routine-detail-view {
          display: flex;
          flex-direction: column;
          gap: 24px;
        }

        .routine-detail-header {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 20px 0;
        }

        .large-progress {
          position: relative;
          width: 120px;
          height: 120px;
        }

        .progress-ring {
          transform: rotate(-90deg);
        }

        .progress-ring-bg {
          fill: none;
          stroke: var(--divider-color);
          stroke-width: 8;
        }

        .progress-ring-fill {
          fill: none;
          stroke: var(--primary-color);
          stroke-width: 8;
          stroke-linecap: round;
          stroke-dasharray: 339.292;
          transition: stroke-dashoffset 0.5s ease;
        }

        .progress-center {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          text-align: center;
        }

        .progress-number {
          display: block;
          font-size: 32px;
          font-weight: bold;
          color: var(--text-primary);
        }

        .progress-total {
          display: block;
          font-size: 14px;
          color: var(--text-secondary);
        }

        .complete-celebration {
          text-align: center;
          padding: 20px;
        }

        .complete-celebration ha-icon {
          font-size: 64px;
          color: var(--success-color);
          animation: bounce 1s infinite;
        }

        @keyframes bounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-10px); }
        }

        .complete-celebration h3 {
          font-size: 24px;
          color: var(--success-color);
          margin: 12px 0 8px;
        }

        .complete-celebration p {
          color: var(--text-secondary);
          margin: 0;
        }

        .tasks-list {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }

        .task-card {
          display: flex;
          align-items: center;
          gap: 16px;
          padding: 16px;
          background: var(--card-background);
          border: 2px solid var(--divider-color);
          border-radius: 12px;
          transition: all 0.3s;
        }

        .task-card.completed {
          opacity: 0.6;
          border-color: var(--success-color);
        }

        .checkbox-btn {
          background: none;
          border: none;
          padding: 0;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 40px;
          color: var(--text-secondary);
          transition: color 0.2s;
        }

        .task-card.completed .checkbox-btn {
          color: var(--success-color);
        }

        .task-image {
          width: 80px;
          height: 80px;
          border-radius: 8px;
          overflow: hidden;
          background: var(--divider-color);
        }

        .task-image img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .task-content {
          flex: 1;
        }

        .task-title {
          margin: 0 0 8px 0;
          font-size: 18px;
          font-weight: bold;
          color: var(--text-primary);
        }

        .task-duration {
          display: inline-flex;
          align-items: center;
          gap: 4px;
          font-size: 14px;
          color: var(--text-secondary);
        }

        .routine-actions {
          display: flex;
          justify-content: center;
          padding: 20px 0;
        }

        .reset-btn {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 12px 24px;
          background: var(--divider-color);
          color: var(--text-primary);
          border: none;
          border-radius: 8px;
          font-size: 16px;
          cursor: pointer;
          transition: background 0.2s;
        }

        .reset-btn:hover {
          background: var(--warning-color);
          color: white;
        }
      </style>
    `;
  }
}

customElements.define('kids-schedule-card', KidsScheduleCard);

// Announce the card to Home Assistant
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'kids-schedule-card',
  name: 'Kids Schedule Card',
  description: 'Child-friendly schedule card with task tracking',
  preview: true,
});

console.info(
  '%c  KIDS-SCHEDULE-CARD  \\n%c  Version 1.0.0  ',
  'color: orange; font-weight: bold; background: black',
  'color: white; font-weight: bold; background: dimgray',
);
