class Articles {
    constructor() {
        this.articlesContainer = document.getElementById('articles-container');
        this.articleForm = document.getElementById('article-form');
        
        this.bindEvents();
    }
    
    bindEvents() {
        if (this.articleForm) {
            this.articleForm.addEventListener('submit', this.handleArticleSubmit.bind(this));
        }
    }
    
    async loadFeaturedArticles() {
        try {
            const response = await fetch('/api/articles?featured=true');
            const articles = await response.json();
            
            if (!response.ok) {
                throw new Error('Не удалось загрузить статьи');
            }
            
            const container = document.getElementById('featured-articles');
            if (container) {
                container.innerHTML = '';
                
                articles.forEach(article => {
                    const articleEl = document.createElement('div');
                    articleEl.className = 'article-card';
                    articleEl.innerHTML = `
                        <h3>${article.title}</h3>
                        <p>${article.excerpt}</p>
                        ${article.plant_name ? `<p>Растение: ${article.plant_name}</p>` : ''}
                        <button class="btn btn-outline btn-small" onclick="articles.showArticleDetails(${article.id})">Читать</button>
                    `;
                    container.appendChild(articleEl);
                });
            }
            
        } catch (error) {
            console.error('Ошибка при загрузке статей:', error);
        }
    }
    
    async loadAllArticles() {
        try {
            const response = await fetch('/api/articles');
            const articles = await response.json();
            
            if (!response.ok) {
                throw new Error('Не удалось загрузить статьи');
            }
            
            if (this.articlesContainer) {
                this.articlesContainer.innerHTML = '';
                
                articles.forEach(article => {
                    const articleEl = document.createElement('div');
                    articleEl.className = 'article-card';
                    articleEl.innerHTML = `
                        <h3>${article.title}</h3>
                        <p>${article.excerpt}</p>
                        ${article.plant_name ? `<p>Растение: ${article.plant_name}</p>` : ''}
                        <p>Автор: ${article.author}</p>
                        <button class="btn btn-outline btn-small" onclick="articles.showArticleDetails(${article.id})">Читать</button>
                    `;
                    this.articlesContainer.appendChild(articleEl);
                });
            }
            
        } catch (error) {
            console.error('Ошибка при загрузке статей:', error);
        }
    }
    
      async showArticleDetails(articleId) {
    try {
      const response = await fetch(`/api/articles/${articleId}`);
      const article = await response.json();
      
      if (!response.ok) {
        throw new Error(article.error || 'Не удалось загрузить статью');
      }

      // Заполняем модальное окно
      document.getElementById('article-detail-title').textContent = article.title;
      document.getElementById('article-detail-content').innerHTML = 
        article.content.replace(/\n/g, '<br>');
      document.getElementById('article-detail-author').textContent = 
        `Автор: ${article.author}`;
      document.getElementById('article-detail-date').textContent = 
        `Опубликовано: ${this.formatDate(article.created_at)}`;
      
      // Растение (если есть)
      const plantElement = document.getElementById('article-detail-plant');
      if (article.plant_name) {
        plantElement.textContent = `Растение: ${article.plant_name}`;
        plantElement.style.display = 'block';
      } else {
        plantElement.style.display = 'none';
      }

      showModal('article-details-modal');
    } catch (error) {
      console.error('Ошибка при загрузке статьи:', error);
      showErrorNotification(error.message);
    }
  }

  formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('ru-RU', options);
  }
    
    async handleArticleSubmit(e) {
        e.preventDefault();
        
        if (!auth.user) {
            showLoginModal();
            return;
        }
        
        const title = document.getElementById('article-title').value;
        const content = document.getElementById('article-content').value;
        const plantId = document.getElementById('article-plant').value || null;
        const isFeatured = document.getElementById('article-featured').checked;
        
        if (!title || !content) {
            alert('Пожалуйста, заполните заголовок и содержание статьи');
            return;
        }
        
        try {
            const response = await fetch('/api/articles', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...auth.getAuthHeader()
                },
                body: JSON.stringify({
                    title,
                    content,
                    plant_id: plantId,
                    is_featured: isFeatured
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Не удалось создать статью');
            }
            
            alert('Статья успешно создана!');
            
            // Обновляем список статей
            this.loadAllArticles();
            this.loadFeaturedArticles();
            
            // Очищаем форму
            this.articleForm.reset();
            
        } catch (error) {
            console.error('Ошибка при создании статьи:', error);
            alert(error.message);
        }
    }
}

const articles = new Articles();