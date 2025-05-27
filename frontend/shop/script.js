document.addEventListener('DOMContentLoaded', function() {
    const serviceButtons = document.querySelectorAll('.uslugi');
    const bioButtons = document.querySelectorAll('.biograf');
    const allServiceCatalogs = document.querySelectorAll('.kataloguslug');
    const allBioCatalogs = document.querySelectorAll('.bio-catalog');
    
    // Скрываем все каталоги при загрузке
    allServiceCatalogs.forEach((catalog, index) => {
        if (index !== 0) {
            catalog.classList.remove('active');
        }
    });
    allBioCatalogs.forEach(catalog => catalog.classList.remove('active'));
    
    // Обработчики для кнопок "Услуги"
    serviceButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Скрываем все каталоги
            allServiceCatalogs.forEach(catalog => catalog.classList.remove('active'));
            allBioCatalogs.forEach(catalog => catalog.classList.remove('active'));
            
            // Показываем нужный каталог услуг
            const serviceId = this.getAttribute('data-service');
            document.getElementById(serviceId).classList.add('active');
            
            // Обновляем активные кнопки
            serviceButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            bioButtons.forEach(btn => btn.classList.remove('active'));
        });
    });
    
    // Обработчики для кнопок "Биография"
    bioButtons.forEach((button, index) => {
        button.addEventListener('click', function() {
            // Скрываем все каталоги
            allServiceCatalogs.forEach(catalog => catalog.classList.remove('active'));
            allBioCatalogs.forEach(catalog => catalog.classList.remove('active'));
            
            // Показываем нужную биографию
            const bioId = 'bio' + (index + 1);
            document.getElementById(bioId).classList.add('active');
            
            // Обновляем активные кнопки
            serviceButtons.forEach(btn => btn.classList.remove('active'));
            bioButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // По умолчанию показываем услуги первого пользователя
    document.querySelector('.uslugi').click();
});



    // ЧЕКБОКСЫ
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