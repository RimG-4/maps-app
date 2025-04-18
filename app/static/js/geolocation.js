function initGeolocation() {
    // Проверка наличия библиотеки Leaflet и карты
    if (typeof L === 'undefined') {
        console.error('Библиотека карт не загружена!');
        return;
    }

    if (!window.map) {
        console.warn('Карта не инициализирована (window.map отсутствует)');
        return;
    }

    // Проверка поддержки геолокации
    if (!navigator.geolocation) {
        console.warn('Браузер не поддерживает геолокацию');
        alert('Ваш браузер не поддерживает геолокацию.');
        return;
    }

    // Запрос геопозиции
    navigator.geolocation.getCurrentPosition(
        position => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            console.log('Текущая позиция:', lat, lon);

            // Сохраняем данные глобально
            window.userLocation = { lat, lon };

            // Добавляем маркер на карту
            const marker = L.marker([lat, lon], {
                icon: L.divIcon({
                    className: 'user-location-marker',
                    html: '<div class="pulse-dot"></div>',
                    iconSize: [20, 20]
                })
            }).addTo(window.map);

            marker.bindPopup(`Вы здесь: ${lat.toFixed(5)}, ${lon.toFixed(5)}`)
                  .openPopup();

            // Центрируем карту
            window.map.setView([lat, lon], 15);

            // Получаем адрес
            fetch(`/get_address?lat=${lat}&lon=${lon}`)
                .then(response => {
                    if (!response.ok) throw new Error('Ошибка сети');
                    return response.json();
                })
                .then(data => {
                    window.userAddress = data.address;
                    console.log('Текущий адрес:', data.address);
                })
                .catch(error => {
                    console.error('Ошибка при получении адреса:', error);
                });
        },
        error => {
            const messages = {
                [error.PERMISSION_DENIED]: 'Вы запретили доступ к геолокации',
                [error.POSITION_UNAVAILABLE]: 'Информация о местоположении недоступна',
                [error.TIMEOUT]: 'Истекло время ожидания геолокации',
                [error.UNKNOWN_ERROR]: 'Неизвестная ошибка геолокации'
            };
            
            const message = messages[error.code] || 'Ошибка при определении местоположения';
            console.error('Ошибка геолокации:', message, error);
        },
        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    );
}

// Инициализация после полной загрузки страницы
if (document.readyState === 'complete') {
    initGeolocation();
} else {
    window.addEventListener('load', initGeolocation);
}