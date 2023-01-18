(function(){
    var select = document.querySelector('#indexes');
    if (localStorage.selectedIndex !== undefined) {
        select.selectedIndex = localStorage.selectedIndex;
    }
    select.onchange = function() {
        localStorage.selectedIndex = this.selectedIndex;
    }
})()


document.addEventListener("DOMContentLoaded", function () { // событие загрузки страницы
    // выбираем на странице все элементы типа textarea и input, select
    document.querySelectorAll('textarea, input, select').forEach(function (e) {
        // если данные значения уже записаны в sessionStorage, то вставляем их в поля формы
        // путём этого мы как раз берём данные из памяти браузера, если страница была случайно перезагружена
        if (e.value === '') e.value = window.sessionStorage.getItem(e.name, e.value);
        // на событие ввода данных (включая вставку с помощью мыши) вешаем обработчик
        e.addEventListener('input', function () {
            // и записываем в sessionStorage данные, в качестве имени используя атрибут name поля элемента ввода
            window.sessionStorage.setItem(e.name, e.value);
        })
        e.addEventListener('select', function () {
            document.getElementById('indexes').onchange = function () {
                localStorage['Item'] = this.value;
            };
        })
    })
});

