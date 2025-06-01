class Auth {
  constructor() {
    this.token = localStorage.getItem("token");
    this.user = JSON.parse(localStorage.getItem("user") || "null");
    this._isAuthenticating = false;

    this.initElements();
    this.bindEvents();
  }

  initElements() {
    this.loginForm = document.getElementById("login-form");
    this.registerForm = document.getElementById("register-form");
    this.profileForm = document.getElementById("profile-form");
    this.logoutBtn = document.getElementById("logout-btn");
  }

  bindEvents() {
    if (this.loginForm) {
      this.loginForm.addEventListener("submit", (e) => this.handleLogin(e));
    }

    if (this.registerForm) {
      this.registerForm.addEventListener("submit", (e) =>
        this.handleRegister(e)
      );
    }

    if (this.profileForm) {
      this.profileForm.addEventListener("submit", (e) =>
        this.handleProfileUpdate(e)
      );
    }

    if (this.logoutBtn) {
      this.logoutBtn.addEventListener("click", (e) => this.handleLogout(e));
    }
  }

  async handleLogin(e) {
    e.preventDefault();
    if (this._isAuthenticating) return;
    this._isAuthenticating = true;

    try {
      const email = document.getElementById("login-email").value;
      const password = document.getElementById("login-password").value;

      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.status === 401) {
        throw new Error("Неверные учетные данные");
      }

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Ошибка входа");
      }

      this.setAuthData(data.token, data.user);
      updateUserUI();

      // Не вызываем loadUserPlants здесь - это сделает showPage
      hideModal('login-modal')
      showPage("dashboard");
    } catch (error) {
      console.error("Ошибка входа:", error);
      showErrorNotification(error.message);
    } finally {
      this._isAuthenticating = false;
    }
  }

  setAuthData(token, user) {
    this.token = token;
    this.user = user;
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));
  }

  isTokenValid() {
  if (!this.token) return false;
  try {
    const payload = JSON.parse(atob(this.token.split('.')[1]));
    if (!payload.exp) return false;
    return payload.exp * 1000 > Date.now();
  } catch (error) {
    console.error("Ошибка проверки токена:", error);
    return false;
  }
}

  getAuthHeader() {
    if (!this.token || !this.isTokenValid()) {
      this.handleLogout();
      throw new Error("Требуется авторизация");
    }
    console.log("Используемый токен:", this.token); 
    return {
      'Authorization': `Bearer ${this.token}`,
      "Content-Type": "application/json",
    };
  }

  async handleRegister(e) {
    e.preventDefault();

    const name = document.getElementById("register-name").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const confirm = document.getElementById("register-confirm").value;

    if (password !== confirm) {
      alert("Пароли не совпадают");
      return;
    }

    try {
      const response = await fetch("/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: name,
          email,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Ошибка регистрации");
      }

    this.setAuthData(data.token, data.user);
    updateUserUI();
    hideModal("register-modal");
    showPage("home");
  } catch (error) {
    console.error("Ошибка регистрации:", error);
    showErrorNotification(error.message);
  }
  }

  async handleProfileUpdate(e) {
    e.preventDefault();
    if (this._isAuthenticating) return;
    this._isAuthenticating = true;

    const name = document.getElementById("profile-name").value;
    const email = document.getElementById("profile-email").value;
    const password = document.getElementById("profile-password").value;

    try {
      // Проверяем валидность токена
      if (!this.isTokenValid()) {
        this.handleLogout();
        throw new Error("Сессия истекла. Пожалуйста, войдите снова.");
      }

      const response = await fetch("/api/auth/profile", {
        method: "PUT",
        headers: this.getAuthHeader(), // Используем метод getAuthHeader()
        body: JSON.stringify({
          username: name,
          email,
          password: password || undefined,
        }),
      });

      if (response.status === 401) {
        // Если токен недействителен, разлогиниваем пользователя
        this.handleLogout();
        throw new Error("Сессия истекла. Пожалуйста, войдите снова.");
      }

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Ошибка обновления профиля");
      }

      // Обновляем данные пользователя
      this.user.username = name;
      this.user.email = email;
      localStorage.setItem("user", JSON.stringify(this.user));

      showPage("home");
    } catch (error) {
      console.error("Ошибка при обновлении профиля:", error);
      showErrorNotification(error.message);
    } finally {
      this._isAuthenticating = false;
    }
  }

  async handleLogout(e) {
    // Добавляем параметр по умолчанию
    if (e) e.preventDefault();

    try {
      if (this.token) {
        await fetch("/api/auth/logout", {
          method: "POST",
          headers: { Authorization: `Bearer ${this.token}` },
        });
      }

      this.clearAuthData();
      updateUserUI();
      showPage("home");
    } catch (error) {
      console.error("Ошибка при выходе:", error);
      this.clearAuthData(); // Все равно очищаем данные
      updateUserUI();
      showPage("home");
    }
  }

  clearAuthData() {
    this.token = null;
    this.user = null;
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }
}

const auth = new Auth();

// Обновление UI в зависимости от состояния авторизации
function updateUserUI() {
  const loginBtn = document.getElementById("login-btn");
  const registerBtn = document.getElementById("register-btn");
  const logoutBtn = document.getElementById("logout-btn");
  const profileBtn = document.getElementById("profile-btn");

  if (auth.user) {
    // Пользователь авторизован
    if (loginBtn) loginBtn.style.display = "none";
    if (registerBtn) registerBtn.style.display = "none";
    if (logoutBtn) logoutBtn.style.display = "inline-block";
    if (profileBtn) profileBtn.style.display = "inline-block";

    // Заполняем данные профиля
    if (document.getElementById("profile-name")) {
      document.getElementById("profile-name").value = auth.user.username;
      document.getElementById("profile-email").value = auth.user.email;
    }
  } else {
    // Пользователь не авторизован
    if (loginBtn) loginBtn.style.display = "inline-block";
    if (registerBtn) registerBtn.style.display = "inline-block";
    if (logoutBtn) logoutBtn.style.display = "none";
    if (profileBtn) profileBtn.style.display = "none";
  }
}
