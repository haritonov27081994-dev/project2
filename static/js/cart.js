document.addEventListener('DOMContentLoaded', () => {
  // Получаем CSRF-токен из cookie браузера для безопасного POST-запроса в Django
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie('csrftoken');
  const cartCounter = document.getElementById('cart-counter');
  const messagesContainer = document.getElementById('messages-container');

  // Функция для показа всплывающего уведомления без перезагрузки страницы
  function showAlert(text) {
    if (!messagesContainer) return;

    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success';
    alertDiv.innerHTML = `
      <span>${text}</span>
      <button type="button" class="alert-close" onclick="this.parentElement.remove();">&times;</button>
    `;
    messagesContainer.appendChild(alertDiv);

    // Автоматически скрываем уведомление через 3.5 секунды
    setTimeout(() => {
      alertDiv.remove();
    }, 3500);
  }

  // Навешиваем обработчик на все кнопки "Добавить в корзину"
  const addButtons = document.querySelectorAll('.js-add-to-cart');

  addButtons.forEach((button) => {
    button.addEventListener('click', async () => {
      const url = button.dataset.url;
      const originalText = button.textContent;

      button.disabled = true;
      button.textContent = 'Добавляем...';

      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
          },
        });

        if (!response.ok) {
          throw new Error('Ошибка при добавлении товара');
        }

        const data = await response.json();

        if (data.status === 'ok') {
          // Обновляем цифру счетчика в шапке
          if (cartCounter) {
            cartCounter.textContent = data.total_items;
            cartCounter.classList.add('bump');
            setTimeout(() => cartCounter.classList.remove('bump'), 300);
          }

          // Показываем уведомление
          showAlert(data.message);
        }
      } catch (error) {
        console.error(error);
        alert('Не удалось добавить товар в корзину. Попробуйте обновить страницу.');
      } finally {
        button.disabled = false;
        button.textContent = originalText;
      }
    });
  });
});
