class Plants {
  constructor() {
    this._isLoading = false;
    this.currentPlantDetailsId = null;
    this.currentDeletePlantId = null;
    this.initDeleteHandlers();
    this.initElements();
    this.bindEvents();
  }

  initDeleteHandlers() {
    const deleteBtn = document.getElementById("confirm-delete-plant");
    if (deleteBtn) {
      deleteBtn.addEventListener("click", this.handleDeletePlant.bind(this));
    }
  }

  initElements() {
    this.addPlantForm = document.getElementById("add-plant-form");
    this.wateringForm = document.getElementById("watering-form");
  }

  bindEvents() {
    if (this.addPlantForm) {
      this.addPlantForm.addEventListener(
        "submit",
        this.handleAddPlant.bind(this)
      );
    }

    if (this.wateringForm) {
      this.wateringForm.addEventListener(
        "submit",
        this.handleWatering.bind(this)
      );
    }
  }

  showDeleteConfirmation(plantId, event) {
    if (event) event.stopPropagation();
    this.currentDeletePlantId = plantId;
    showModal("delete-plant-modal");
  }

  async loadAllPlants() {
    try {
      const response = await fetch("/api/plants");
      const plants = await response.json();

      if (!response.ok) {
        throw new Error("Не удалось загрузить растения");
      }

      const grid = document.getElementById("all-plants-grid");
      grid.innerHTML = "";

      // Загружаем растения пользователя для проверки, какие уже добавлены
      let userPlants = [];
      if (auth.user) {
        const userResponse = await fetch("/api/user/plants", {
          headers: auth.getAuthHeader(),
        });

        if (userResponse.ok) {
          userPlants = await userResponse.json();
        }
      }

      plants.forEach((plant) => {
        const isAdded = userPlants.some((p) => p.plant_id === plant.id);

        const card = document.createElement("div");
        card.className = "plant-card";
        card.innerHTML = `
                    <div class="plant-image" style="background-image: url('${
                      plant.image_url
                    }')"></div>
                    <div class="plant-info">
                        <h3>${plant.name}</h3>
                        <p>Тип: ${plant.type}</p>
                        <div class="plant-actions">
                            ${
                              isAdded
                                ? '<span class="plant-status status-ok">Уже добавлено</span>'
                                : `<button class="btn btn-primary btn-small" onclick="plants.addToMyPlants('${plant.id}', event)">Добавить</button>`
                            }
                            <button class="btn btn-outline btn-small" onclick="plants.showPlantDetails('${
                              plant.id
                            }', event)">Подробнее</button>
                        </div>
                    </div>
                `;
        grid.appendChild(card);
      });
    } catch (error) {
      console.error("Ошибка при загрузке растений:", error);
      alert(error.message);
    }
  }

  async loadUserPlants() {
    if (this._isLoading || !auth.user) return;
    this._isLoading = true;

    try {
      console.log("Начало загрузки растений пользователя");

      if (!auth.isTokenValid()) {
        auth.handleLogout();
        throw new Error("Сессия истекла");
      }

      const response = await fetch("/api/user/plants", {
        headers: auth.getAuthHeader(),
      });

      if (response.status === 401) {
        auth.handleLogout();
        throw new Error("Сессия истекла");
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Ошибка сервера");
      }

      const plants = await response.json();
      this.renderUserPlants(plants);
    } catch (error) {
      console.error("Ошибка загрузки растений:", error);
      if (!error.message.includes("Сессия истекла")) {
        showErrorNotification("Не удалось загрузить ваши растения");
      }
    } finally {
      this._isLoading = false;
    }
  }

  renderUserPlants(plants) {
    const grid = document.getElementById("my-plants-grid");
    if (!grid) return;
    grid.innerHTML = "";
    plants.forEach((plant) => {
      const lastWatered = plant.last_watered
        ? `Последний полив: ${formatDate(plant.last_watered)}`
        : "Полив не указан";

      const nextWatering = plant.next_watering
        ? `Следующий полив: ${formatDate(plant.next_watering)}`
        : "Частота полива не указана";

      const card = document.createElement("div");
      card.className = "plant-card";
      card.innerHTML = `
        <div class="plant-image" style="background-image: url('${plant.image_url}')"></div>
        <div class="plant-info">
          <h3>${plant.name}</h3>
          <p>${lastWatered}</p>
          <p>${nextWatering}</p>
          <div class="plant-actions">
            <button class="btn btn-primary btn-small" 
                    onclick="plants.showWateringModal('${plant.id}', event)">
              Отметить полив
            </button>
            <button class="btn btn-outline btn-small" 
                    onclick="plants.showPlantDetails('${plant.plant_id}', event)">
              Подробнее
            </button>
            <button class="btn btn-danger btn-small" 
                    onclick="plants.showDeleteConfirmation('${plant.id}', event)">
              Удалить
            </button>
          </div>
        </div>
      `;
      grid.appendChild(card);
    });
  }

  async addToMyPlants(plantId, event) {
    if (event) event.stopPropagation();

    if (!auth.user) {
      showLoginModal();
      return;
    }

    try {
      const response = await fetch("/api/user/plants", {
        method: "POST",
        headers: auth.getAuthHeader(),
        body: JSON.stringify({ plant_id: plantId }),
      });

      if (response.status === 401) {
        auth.handleLogout();
        throw new Error("Сессия истекла");
      }

      const data = await response.json();

      if (response.status === 400) {
        // Обработка случая, когда растение уже добавлено
        showInfoNotification(data.error || "Растение уже в вашей коллекции");
        return;
      }

      if (!response.ok) {
        throw new Error(data.error || "Ошибка при добавлении");
      }

      this.loadAllPlants();
      this.loadUserPlants();
    } catch (error) {
      console.error("Ошибка при добавлении растения:", error);
      if (!error.message.includes("Сессия истекла")) {
        showErrorNotification(error.message);
      }
    }
  }

  async showPlantDetails(plantId, event) {
    if (event) event.stopPropagation();

    try {
      const response = await fetch(`/api/plants/${plantId}`);

      if (response.status === 404) {
        throw new Error("Растение не найдено в базе данных");
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Ошибка загрузки информации");
      }

      const plant = await response.json();
      this.currentPlantDetailsId = plantId;

      // Обновляем UI
      document.getElementById("detail-plant-name").textContent = plant.name;
      document.getElementById(
        "detail-plant-type"
      ).textContent = `Тип: ${plant.type}`;
      document.getElementById("detail-plant-care").textContent =
        plant.care_instructions;
      document.getElementById("detail-temperature").textContent =
        plant.optimal_temperature;

      const imageElement = document.getElementById("detail-plant-image");
      if (imageElement) {
        imageElement.style.backgroundImage = `url('${plant.image_url}')`;
      }

      // Проверяем, есть ли растение у пользователя
      if (auth.user) {
        try {
          const userResponse = await fetch("/api/user/plants", {
            headers: auth.getAuthHeader(),
          });

          if (userResponse.ok) {
            const userPlants = await userResponse.json();
            const userPlant = userPlants.find((p) => p.plant_id == plantId);

            if (userPlant) {
              const lastWatered = userPlant.last_watered
                ? formatDate(userPlant.last_watered)
                : "не указан";
              document.getElementById("detail-last-watered").textContent =
                lastWatered;
            }
          }
        } catch (error) {
          console.error("Ошибка при загрузке данных полива:", error);
        }
      }

      showModal("plant-details-modal");
    } catch (error) {
      console.error("Ошибка при загрузке деталей растения:", error);
      showErrorNotification(error.message);
    }
  }

  showWateringModalFromDetails() {
    if (!this.currentPlantDetailsId) return;
    hideModal("plant-details-modal");
    this.showWateringModal(this.currentPlantDetailsId);
  }

  async showWateringModal(plantId, event) {
    if (event) event.stopPropagation();

    try {
      if (!auth.user) {
        showLoginModal();
        return;
      }

      const response = await fetch("/api/user/plants", {
        headers: auth.getAuthHeader(),
      });

      if (!response.ok) {
        throw new Error("Не удалось загрузить ваши растения");
      }

      const userPlants = await response.json();
      const userPlant = userPlants.find(
        (p) => p.id == plantId || p.plant_id == plantId
      );

      if (!userPlant) {
        showNotification("Растение не найдено в вашей коллекции", "error");
        return;
      }

      // Устанавливаем ID растения для полива
      this.currentWateringPlantId = userPlant.id;

      // Заполняем форму
      document.getElementById("watering-date").value = userPlant.last_watered
        ? userPlant.last_watered.split("T")[0]
        : new Date().toISOString().split("T")[0];

      document.getElementById("watering-interval").value =
        userPlant.watering_interval || 7;

      showModal("watering-modal");
    } catch (error) {
      console.error("Ошибка при открытии формы полива:", error);
    }
  }

  async handleWatering(e) {
    e.preventDefault();

    try {
      // Проверяем, что растение выбрано
      if (!this.currentWateringPlantId) {
        throw new Error("Не выбрано растение для полива");
      }

      const date = document.getElementById("watering-date").value;
      const interval = parseInt(
        document.getElementById("watering-interval").value
      );

      const response = await fetch(
        `/api/user/plants/${this.currentWateringPlantId}/water`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${auth.token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            date: date,
            interval: interval,
          }),
        }
      );

      if (response.status === 401) {
        auth.handleLogout();
        throw new Error("Сессия истекла");
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Ошибка при сохранении");
      }

      // Используем showNotification вместо showSuccessNotification
      this.loadUserPlants();
      hideModal("watering-modal");
    } catch (error) {
      console.error("Ошибка при сохранении полива:", error);
    }
  }

  async handleAddPlant(e) {
    e.preventDefault();

    const name = document.getElementById("plant-name").value;
    const type = document.getElementById("plant-type").value;
    const photo = document.getElementById("plant-photo").files[0];

    if (!name || !type) {
      alert("Пожалуйста, заполните все обязательные поля");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("name", name);
      formData.append("type", type);
      if (photo) formData.append("photo", photo);

      const response = await fetch("/api/plants", {
        method: "POST",
        headers: auth.getAuthHeader(),
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Не удалось добавить растение");
      }

      alert(`Растение "${name}" успешно добавлено!`);

      // Обновляем список растений
      this.loadAllPlants();
      this.loadUserPlants();

      // Закрываем модальное окно
      hideModal("add-plant-modal");
    } catch (error) {
      console.error("Ошибка при добавлении растения:", error);
      alert(error.message);
    }
  }

  // Добавляем новый метод в класс Plants
  async loadUserPlantsForReminders() {
    if (!auth.user) return;

    try {
      const response = await fetch("/api/user/plants", {
        headers: auth.getAuthHeader(),
      });

      const plants = await response.json();

      if (!response.ok) {
        throw new Error("Не удалось загрузить ваши растения");
      }

      // Заполняем выпадающий список растений в форме напоминаний
      const plantSelect = document.getElementById("reminder-plant");
      if (plantSelect) {
        plantSelect.innerHTML = '<option value="">Выберите растение</option>';

        plants.forEach((plant) => {
          const option = document.createElement("option");
          option.value = plant.id;
          option.textContent = plant.name;
          plantSelect.appendChild(option);
        });
      }
    } catch (error) {
      console.error("Ошибка при загрузке растений для напоминаний:", error);
    }
  }

  async handleDeletePlant() {
    if (!this.currentDeletePlantId) return;

    try {
      // Check token validity first
      if (!auth.isTokenValid()) {
        auth.handleLogout();
        throw new Error("Сессия истекла");
      }

      const response = await fetch(
        `/api/user/plants/${this.currentDeletePlantId}`,
        {
          method: "DELETE",
          headers: auth.getAuthHeader(),
        }
      );

      if (response.status === 401) {
        auth.handleLogout();
        throw new Error("Сессия истекла");
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Не удалось удалить растение");
      }

      this.loadUserPlants();
      hideModal("delete-plant-modal");
    } catch (error) {
      console.error("Ошибка при удалении растения:", error);
      showErrorNotification(error.message);
    }
  }
}

const plants = new Plants();

// Вспомогательные функции
function formatDate(dateString) {
  if (!dateString) return "не указано";

  const date = new Date(dateString);
  return date.toLocaleDateString("ru-RU");
}

window.plants = new Plants();
