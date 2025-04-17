document.addEventListener("DOMContentLoaded", () => {

    if (typeof L === 'undefined') {
        console.error('Карта не открывается!');
        alert('Ошибка загрузки карты. Пожалуйста, обновите страницу.');
        return;
    }

    if (!window.map) {
        console.warn("Карта ещё не загружена (window.map отсутствует)");
        return;
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                console.log("Текущая позиция:", lat, lon);

                // Сохраняем глобально
                window.userLocation = { lat, lon };

                L.marker([lat, lon]).addTo(window.map)
                    .bindPopup(`Вы здесь: ${lat.toFixed(5)}, ${lon.toFixed(5)}`)
                    .openPopup();

                window.map.setView([lat, lon], 15);

                fetch(`/get_address?lat=${lat}&lon=${lon}`)
                    .then(response => response.json())
                    .then(data => {
                        alert("Вы находитесь по адресу: " + data.address);
                        window.userAddress = data.address;
                    })
                    .catch(error => console.error("Ошибка при получении адреса:", error));
            },
            error => {
                let message = "";
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        message = "Вы запретили доступ к геолокации.";
                        break;
                    case error.POSITION_UNAVAILABLE:
                        message = "Информация о местоположении недоступна.";
                        break;
                    case error.TIMEOUT:
                        message = "Истекло время ожидания ответа от службы геолокации.";
                        break;
                    default:
                        message = "Неизвестная ошибка при определении местоположения.";
                        break;
                }
                alert(message);
                console.error("Ошибка геолокации:", message, error);
            }
        );
    } else {
        alert("Ваш браузер не поддерживает геолокацию.");
    }

});
