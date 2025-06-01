class Reminders {
  constructor() {
    this.remindersContainer = document.getElementById("reminders-container");
    this.addReminderForm = document.getElementById("add-reminder-form");
    this.editReminderForm = document.getElementById("edit-reminder-form");

    this.bindEvents();
  }

  bindEvents() {
    if (this.addReminderForm) {
      this.addReminderForm.addEventListener(
        "submit",
        this.handleAddReminder.bind(this)
      );
    }

    if (this.editReminderForm) {
      this.editReminderForm.addEventListener(
        "submit",
        this.handleUpdateReminder.bind(this)
      );
    }
  }

  async loadUserReminders() {
    if (!auth.user) return;

    try {
      showLoader();
      const response = await fetch("/api/reminders", {
        headers: auth.getAuthHeader(),
      });

      const reminders = await response.json();

      if (!response.ok) {
        throw new Error(reminders.error || "Не удалось загрузить напоминания");
      }

      if (this.remindersContainer) {
        this.remindersContainer.innerHTML = "";

        if (reminders.length === 0) {
          this.remindersContainer.innerHTML = `
                        <div class="empty-state">
                            <i class="far fa-bell-slash"></i>
                            <p>У вас пока нет напоминаний</p>
                            <button class="btn btn-primary" onclick="showModal('add-reminder-modal')">
                                Создать напоминание
                            </button>
                        </div>
                    `;
          return;
        }

        reminders.forEach((reminder) => {
          const reminderEl = this.createReminderElement(reminder);
          this.remindersContainer.appendChild(reminderEl);
        });
      }
    } catch (error) {
      console.error("Ошибка при загрузке напоминаний:", error);
    } finally {
      hideLoader();
    }
  }

  createReminderElement(reminder) {
    const reminderEl = document.createElement("div");
    reminderEl.className = `reminder-card ${
      reminder.is_completed ? "completed" : ""
    }`;

    let plantInfo = "";
    if (reminder.plant) {
      plantInfo = `
                <div class="reminder-plant">
                    <img src="${reminder.plant.image_url}" alt="${reminder.plant.name}">
                    <span>${reminder.plant.name}</span>
                </div>
            `;
    }

    const dueDate = new Date(reminder.due_date);
    const isOverdue = !reminder.is_completed && dueDate < new Date();

    reminderEl.innerHTML = `
            <div class="reminder-header">
                <h4 class="${
                  isOverdue ? "text-danger" : ""
                }">${this.getReminderTypeName(reminder.type)}</h4>
                <span class="reminder-date ${isOverdue ? "text-danger" : ""}">
                    ${this.formatDateTime(reminder.due_date)}
                    ${isOverdue ? " (Просрочено)" : ""}
                </span>
            </div>
            ${plantInfo}
            ${
              reminder.notes
                ? `<p class="reminder-notes">${reminder.notes}</p>`
                : ""
            }
            <div class="reminder-actions">
                <button class="btn btn-small ${
                  reminder.is_completed ? "btn-outline" : "btn-primary"
                }" 
                    onclick="reminders.toggleReminderCompletion(${
                      reminder.id
                    }, ${!reminder.is_completed})">
                    ${
                      reminder.is_completed
                        ? "Отметить невыполненным"
                        : "Выполнить"
                    }
                </button>
                <button class="btn btn-outline btn-small" onclick="reminders.showEditReminderModal(${
                  reminder.id
                })">
                    Редактировать
                </button>
                <button class="btn btn-outline btn-small" onclick="reminders.deleteReminder(${
                  reminder.id
                })">
                    Удалить
                </button>
            </div>
        `;

    return reminderEl;
  }

  getReminderTypeName(type) {
    const types = {
      watering: "Полив",
      fertilizing: "Удобрение",
      pruning: "Обрезка",
      repotting: "Пересадка",
      other: "Другое",
    };
    return types[type] || type;
  }

  formatDateTime(dateTimeString) {
    if (!dateTimeString) return "не указано";

    const date = new Date(dateTimeString);

    // Форматирование даты: DD.MM.YYYY HH:MM
    const day = date.getDate().toString().padStart(2, "0");
    const month = (date.getMonth() + 1).toString().padStart(2, "0");
    const year = date.getFullYear();
    const hours = date.getHours().toString().padStart(2, "0");
    const minutes = date.getMinutes().toString().padStart(2, "0");

    return `${day}.${month}.${year} ${hours}:${minutes}`;
  }

  async toggleReminderCompletion(reminderId, isCompleted) {
    try {
      const response = await fetch(`/api/reminders/${reminderId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth.token}`,
        },
        body: JSON.stringify({ is_completed: isCompleted }),
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.message || "Ошибка сервера");
      }

      this.loadUserReminders();
    } catch (error) {
      console.error("Ошибка:", error);
      showNotification(error.message, "error");
    }
  }

  async showEditReminderModal(reminderId) {
    try {
      console.log("Opening edit modal for reminder:", reminderId); // Логирование

      // 1. Получаем данные напоминания
      const response = await fetch(`/api/reminders/${reminderId}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${auth.token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Не удалось загрузить данные напоминания");
      }

      const reminder = await response.json();
      console.log("Reminder data:", reminder); // Логирование

      // 2. Заполняем форму
      document.getElementById("edit-reminder-id").value = reminder.id;
      document.getElementById("edit-reminder-type").value = reminder.type;
      document.getElementById("edit-reminder-date").value =
        reminder.due_date.slice(0, 16); // Формат datetime-local
      document.getElementById("edit-reminder-notes").value =
        reminder.notes || "";

      // 3. Показываем модальное окно
      showModal("edit-reminder-modal");
    } catch (error) {
      console.error("Ошибка при открытии формы редактирования:", error);
      showNotification(error.message, "error");
    }
  }

  async handleUpdateReminder(e) {
    e.preventDefault();

    const reminderId = document.getElementById("edit-reminder-id").value;
    const type = document.getElementById("edit-reminder-type").value;
    const date = document.getElementById("edit-reminder-date").value;
    const notes = document.getElementById("edit-reminder-notes").value;

    try {
      showLoader();
      const response = await fetch(`/api/reminders/${reminderId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          ...auth.getAuthHeader(),
        },
        body: JSON.stringify({
          type: type,
          due_date: date,
          notes: notes,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Не удалось обновить напоминание");
      }

      this.loadUserReminders();
      hideModal("edit-reminder-modal");
    } catch (error) {
      console.error("Ошибка при обновлении напоминания:", error);
    } finally {
      hideLoader();
    }
  }

  async deleteReminder(reminderId) {
    try {
      const response = await fetch(`/api/reminders/${reminderId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${auth.token}`,
        },
      });

      if (!response.ok) throw new Error("Ошибка удаления");

      this.loadUserReminders();
    } catch (error) {
      console.error("Ошибка:", error);
      showNotification(error.message, "error");
    }
  }

  async handleAddReminder(e) {
    e.preventDefault();

    try {
      const type = document.getElementById("reminder-type").value;
      const date = document.getElementById("reminder-date").value;
      const plantId = document.getElementById("reminder-plant").value || null;
      const notes = document.getElementById("reminder-notes").value;

      if (!type || !date) {
        return;
      }

      showLoader();

      // Явно указываем URL с косой чертой
      const response = await fetch("/api/reminders/", {
        // Добавили / в конце
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth.token}`,
        },
        body: JSON.stringify({
          type: type,
          due_date: date,
          user_plant_id: plantId,
          notes: notes,
        }),
        redirect: "manual", // Отключаем обработку перенаправлений
      });

      // Обработка HTTP ошибок
      if (response.status >= 400) {
        const errorText = await response.text();
        let errorMsg = `Ошибка сервера: ${response.status}`;

        try {
          const errorJson = JSON.parse(errorText);
          errorMsg = errorJson.error || errorMsg;
        } catch {
          if (errorText.includes("DOCTYPE")) {
            errorMsg = "Ошибка конфигурации сервера";
          } else {
            errorMsg = errorText || errorMsg;
          }
        }

        throw new Error(errorMsg);
      }

      const data = await response.json();
      this.loadUserReminders();
      this.addReminderForm.reset();
      hideModal("add-reminder-modal");
    } catch (error) {
      console.error("Ошибка при создании напоминания:", error);
    } finally {
      hideLoader();
    }
  }
}

// Добавьте в конец reminders.js
window.formatDateTime = formatDateTime;

// В конце reminders.js
window.reminders = new Reminders(); // Явно создаем глобальную переменную
