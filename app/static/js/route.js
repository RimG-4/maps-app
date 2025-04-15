document.addEventListener("DOMContentLoaded", () => {
    const fromInput = document.getElementById("from");
    const toInput = document.getElementById("to");
    const buildBtn = document.getElementById("build-route");

    buildBtn.addEventListener("click", () => {
        const from = fromInput.value;
        const to = toInput.value;

        let startAddress = from;
        if (!startAddress && window.userAddress) {
            startAddress = window.userAddress; // Используем полученный адрес
            fromInput.value = startAddress; // Автозаполняем поле
        }

        fetch('/get_route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ from: startAddress, to: to })
        })
            .then(response => response.json())
            .then(data => {
                // тут код отображения маршрута
                console.log("Маршрут:", data);
            })
            .catch(error => {
                console.error("Ошибка при построении маршрута:", error);
            });
    });
});
