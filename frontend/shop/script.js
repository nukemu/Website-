document.addEventListener('DOMContentLoaded', function() {
    const themeSwitch = document.querySelector('.switchs');
    const body = document.body;

    // Проверяем сохраненную тему в localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.add(savedTheme);
        themeSwitch.checked = savedTheme === 'dark-theme';
    }

    // Обработчик изменения темы
    themeSwitch.addEventListener('change', function() {
        if (this.checked) {
            body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark-theme');
        } else {
            body.classList.remove('dark-theme');
            localStorage.setItem('theme', '');
        }
    });
});

for (let i = 1, n = 0; i <= 10; i++, n++) {
        console.log('Итерация № ' + i, ' = ', n);
    }