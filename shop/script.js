
document.addEventListener('DOMContentLoaded', function() {
    // Получаем все вкладки с разработчиками
    const peopleCards = document.querySelectorAll('.people-card');
    // Получаем все разделы с услугами
    const serviceSections = document.querySelectorAll('.kataloguslug');

    // Обработчик для переключения между разработчиками
    peopleCards.forEach(card => {
        card.addEventListener('click', function(e) {
            e.preventDefault();
            // Удаляем активный класс у всех карточек
            peopleCards.forEach(c => c.classList.remove('active'));
            // Добавляем активный класс текущей карточке
            this.classList.add('active');
            
            // Получаем data-атрибут для определения какой раздел показать
            const serviceId = this.getAttribute('data-service');
            
            // Скрываем все разделы
            serviceSections.forEach(section => {
                section.classList.remove('active');
            });
            
            // Показываем нужный раздел
            document.getElementById(serviceId).classList.add('active');
        });
    });

    // Для каждого раздела услуг настраиваем свои чекбоксы
    serviceSections.forEach(section => {
        const checkboxes = section.querySelectorAll('.checkbox-input');
        const articleCards = section.querySelectorAll('.article-card');
        
        // Изначально скрываем все карточки в разделе
        articleCards.forEach(card => {
            card.style.display = 'none';
        });

        // Настраиваем обработчики для чекбоксов в этом разделе
        checkboxes.forEach((checkbox, index) => {
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    // Показываем соответствующую карточку
                    articleCards[index].style.display = 'block';
                } else {
                    // Скрываем соответствующую карточку
                    articleCards[index].style.display = 'none';
                }
            });
        });
    });
});

function handleCheckbox(clickedCheckbox) {
    const checkboxes = document.querySelectorAll('input[name="option"]');
    const articleCard = document.querySelector('.article-card');
    
    // Сбрасываем все чекбоксы, кроме текущего
    checkboxes.forEach((checkbox) => {
      if (checkbox !== clickedCheckbox) {
        checkbox.checked = false;
      }
    });
    
    // Управляем отображением article-card для первого чекбокса
    if (clickedCheckbox.id === 'serviceCheckbox') {
      if (clickedCheckbox.checked) {
        articleCard.style.display = 'block';
      } else {
        articleCard.style.display = 'none';
      }
    } else {
      // Скрываем article-card при выборе других чекбоксов
      articleCard.style.display = 'none';
      // Снимаем выделение с первого чекбокса
      document.getElementById('serviceCheckbox').checked = false;
    }
  }
  
  // Инициализация - скрываем article-card при загрузке страницы
  document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.article-card').style.display = 'none';
  });