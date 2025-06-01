window.auth = null;
window.plants = null;
window.articles = null;
window.reminders = null;

function showErrorNotification(message) {
  // Проверяем, есть ли уже уведомление с таким сообщением
  const existing = document.querySelector(".error-notification");
  if (existing && existing.textContent === message) return;

  // Создаем новое уведомление
  const notification = document.createElement("div");
  notification.className = "error-notification";
  notification.textContent = message;

  // Добавляем в DOM
  const container =
    document.getElementById("notifications-container") || document.body;
  container.appendChild(notification);

  // Автоудаление через 5 секунд
  setTimeout(() => {
    notification.remove();
  }, 5000);
}

// Добавьте стили анимации
const style = document.createElement("style");
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
`;
document.head.appendChild(style);

// Показать модальное окно
function showModal(modalId) {
  const modal = document.getElementById(modalId);
  if (!modal) {
    console.error(`Modal #${modalId} not found!`);
    return;
  }
  modal.style.display = "flex";
}

// Скрыть модальное окно
function hideModal(modalId) {
  document.getElementById(modalId).style.display = "none";
}

// Показать окно входа
function showLoginModal() {
  hideModal("register-modal");
  showModal("login-modal");
}

// Показать окно регистрации
function showRegisterModal() {
  hideModal("login-modal");
  showModal("register-modal");
}

// Показать окно добавления растения
function showAddPlantModal() {
  if (!auth.user) {
    showLoginModal();
    return;
  }
  showModal("add-plant-modal");
}

// Обновленная функция showPage
function showPage(pageId) {
  if (
    (pageId === "dashboard" ||
      pageId === "profile" ||
      pageId === "articles" ||
      pageId === "reminders") &&
    !auth.user
  ) {
    showLoginModal();
    return;
  }

  document.getElementById("home-page").style.display = "none";
  document.getElementById("dashboard-page").style.display = "none";
  document.getElementById("profile-page").style.display = "none";
  document.getElementById("articles-page").style.display = "none";
  document.getElementById("reminders-page").style.display = "none";

  document.getElementById(pageId + "-page").style.display = "block";

  // Загружаем соответствующие данные
  switch (pageId) {
    case "dashboard":
      plants.loadUserPlants();
      break;
    case "home":
      plants.loadAllPlants();
      articles.loadFeaturedArticles();
      break;
    case "articles":
      articles.loadAllArticles();
      break;
    case "reminders":
      reminders.loadUserReminders();
      plants.loadUserPlantsForReminders();
      break;
  }
}

function showLoader() {
  const loader = document.createElement("div");
  loader.className = "loader-overlay";
  loader.innerHTML = '<div class="loader"></div>';
  document.body.appendChild(loader);
}

function hideLoader() {
  const loader = document.querySelector(".loader-overlay");
  if (loader) {
    loader.remove();
  }
}

const loaderStyles = document.createElement("style");
loaderStyles.textContent = `
.loader-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(255, 255, 255, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}

.loader {
    border: 5px solid #f3f3f3;
    border-top: 5px solid #00C851;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
`;
document.head.appendChild(loaderStyles);

// Инициализация при загрузке
document.addEventListener("DOMContentLoaded", function () {
  window.auth = new Auth();
  window.plants = new Plants();
  window.reminders = new Reminders();

  // Проверяем токен при загрузке
  if (auth.token && !auth.isTokenValid()) {
    auth.handleLogout();
  } else if (auth.token) {
    // Если токен валиден, загружаем данные
    plants.loadUserPlants();
  }

  // Показываем главную страницу
  showPage("home");

  // Обработчики кнопок
  document.getElementById("login-btn").addEventListener("click", function (e) {
    e.preventDefault();
    showLoginModal();
  });

  document
    .getElementById("register-btn")
    .addEventListener("click", function (e) {
      e.preventDefault();
      showRegisterModal();
    });

  // Загружаем растения для формы напоминаний
});
