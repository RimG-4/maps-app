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
                        // Сохраняем адрес тоже глобально (по желанию)
                        window.userAddress = data.address;
                    })
                    .catch(error => console.error("Ошибка при получении адреса:", error));
            },
            error => {
                alert("Не удалось получить ваше местоположение");
                console.error("Ошибка геолокации:", error);
            }
        );
    } else {
        alert("Ваш браузер не поддерживает геолокацию.");
    }


});
