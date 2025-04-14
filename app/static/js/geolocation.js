document.addEventListener("DOMContentLoaded", () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                console.log("Текущая позиция:", lat, lon);

                L.marker([lat, lon]).addTo(map)
                    .bindPopup(`Вы здесь: ${lat.toFixed(5)}, ${lon.toFixed(5)}`)
                    .openPopup();

                map.setView([lat, lon], 15); // Центрируем карту на пользователя

                // Пример запроса адреса
                fetch(`/get_address?lat=${lat}&lon=${lon}`)
                    .then(response => response.json())
                    .then(data => {
                        alert("Вы находитесь по адресу: " + data.address);
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