let displayedCars = 20;  // Изначально показываем 20 машин

function loadMoreCars() {
    const carItems = document.querySelectorAll('.car-item');
    const totalCars = carItems.length;

    // Показать еще 20 машин или все оставшиеся
    for (let i = displayedCars; i < Math.min(displayedCars + 20, totalCars); i++) {
        carItems[i].style.display = 'flex';
    }

    // Обновить количество показанных машин
    displayedCars += 20;

    // Если показаны все машины, скрыть кнопку "Показать еще"
    if (displayedCars >= totalCars) {
        document.getElementById('show-more').style.display = 'none';
    }
}

// Скрыть машины, которые не должны быть показаны сразу
document.addEventListener('DOMContentLoaded', () => {
    const carItems = document.querySelectorAll('.car-item');
    carItems.forEach((item, index) => {
        if (index >= displayedCars) {
            item.style.display = 'none';
        }
    });
});
