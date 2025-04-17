document.addEventListener("DOMContentLoaded", () => {
    const fromInput = document.getElementById("from_address");
    const toInput = document.getElementById("to_address");
    const routeForm = document.getElementById("routeForm");

    routeForm.addEventListener("submit", event => {
        event.preventDefault(); // Не перезагружаем страницу

        let from = fromInput.value;
        const to = toInput.value;

        // Если пользователь разрешил геолокацию — автозаполняем
        if (!from && window.userAddress) {
            from = window.userAddress;
            fromInput.value = from;
        }

        fetch('/get_route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ from: from, to: to })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Маршрут:", data);
            // TODO: отобразить маршрут на карте
        })
        .catch(error => {
            console.error("Ошибка при построении маршрута:", error);
        });
    });

    // Кнопка определения местоположения
    const getLocationBtn = document.getElementById("getLocationBtn");
    if (getLocationBtn) {
        getLocationBtn.addEventListener("click", () => {
            if (window.userAddress) {
                fromInput.value = window.userAddress;
            } else {
                alert("Геолокация ещё не получена");
            }
        });
    }
});
