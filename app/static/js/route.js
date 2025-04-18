document.addEventListener("DOMContentLoaded", () => {
    // Проверка инициализации (защита от дублирования)
    if (window.mapInitialized) return;
    window.mapInitialized = true;

    // Инициализация карты
    if (!window.map) {
        window.map = L.map('map').setView([54.7388, 55.9721], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(window.map);
    }

    // Инициализация слоев
    window.routeLayer = null;
    window.trafficLayer = L.layerGroup().addTo(window.map);
    window.markersLayer = L.layerGroup().addTo(window.map); // Для камер и перекрытий

    // Элементы управления
    const routeForm = document.getElementById("route-form");
    const fromInput = document.getElementById("from");
    const toInput = document.getElementById("to");
    const distanceElement = document.getElementById("distance");
    const timeElement = document.getElementById("travelTime");
    const getLocationBtn = document.getElementById("getLocationBtn");

    // Иконки
    const icons = {
        camera: L.icon({
            iconUrl: '/static/images/camera.png',
            iconSize: [25, 25],
            iconAnchor: [12, 25]
        }),
        closure: L.icon({
            iconUrl: '/static/images/stop.png',
            iconSize: [30, 30],
            iconAnchor: [15, 30]
        }),
        user: L.divIcon({
            className: 'user-location-marker',
            html: '<div class="pulse-dot"></div>',
            iconSize: [20, 20]
        })
    };

    // Загрузка данных
    loadTrafficData();
    loadMapData();

    // Обработчики событий
    if (routeForm) routeForm.addEventListener("submit", handleFormSubmit);
    if (getLocationBtn) getLocationBtn.addEventListener("click", handleLocationClick);

    // Основные функции
    async function handleFormSubmit(e) {
        e.preventDefault();
        const from = fromInput.value.trim();
        const to = toInput.value.trim();

        if (!from || !to) {
            alert("Заполните оба поля адресов");
            return;
        }

        try {
            const response = await fetch('/get_route', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    from: from || window.userAddress,
                    to
                })
            });

            if (!response.ok) throw new Error(await response.text());
            const data = await response.json();
            if (data.error) throw new Error(data.error);

            updateRouteInfo(data);
            drawRoute(data.route);

        } catch (error) {
            handleRouteError(error.message);
        }
    }

    async function loadTrafficData() {
        try {
            const response = await fetch('/api/traffic');
            if (!response.ok) throw new Error(await response.text());

            window.trafficLayer.clearLayers();
            const trafficData = await response.json();

            trafficData.forEach(point => {
                const color = point.severity === 'high' ? '#FF5252' : '#FFC107';
                L.circleMarker(point.coordinates.split(',').map(Number), {
                    radius: 8,
                    fillColor: color,
                    color: '#FFF',
                    weight: 1,
                    fillOpacity: 0.8
                }).bindPopup(`
                    <strong>Пробка:</strong> ${point.description}<br>
                    <strong>Время:</strong> ${point.time_from}-${point.time_to}<br>
                    <strong>Уровень:</strong> ${point.severity === 'high' ? 'Высокий' : 'Средний'}
                `).addTo(window.trafficLayer);
            });
        } catch (error) {
            console.error('Ошибка загрузки пробок:', error);
        }
    }

    async function loadMapData() {
        try {
            // Камеры
            const cameras = await (await fetch('/api/cameras')).json();
            cameras.forEach(camera => {
                L.marker(camera.coordinates.split(',').map(Number), {
                    icon: icons.camera
                }).bindPopup(`<strong>Камера:</strong> ${camera.type}`).addTo(window.markersLayer);
            });

            // Перекрытия
            const closures = await (await fetch('/api/road_closures')).json();
            closures.forEach(closure => {
                L.marker(closure.coordinates.split(',').map(Number), {
                    icon: icons.closure
                }).bindPopup(`
                    <strong>Перекрытие:</strong> ${closure.type}<br>
                    ${closure.description || ''}
                `).addTo(window.markersLayer);
            });

        } catch (error) {
            console.error('Ошибка загрузки данных:', error);
        }
    }

    function updateRouteInfo(data) {
        if (distanceElement) distanceElement.textContent = `${data.distance} км`;
        if (timeElement) timeElement.textContent = `${data.time} мин`;
        document.getElementById("route-info").style.display = "block";
    }

    function drawRoute(routeCoords) {
        if (window.routeLayer) map.removeLayer(window.routeLayer);

        window.routeLayer = L.polyline(routeCoords, {
            color: '#4CAF50',
            weight: 6,
            opacity: 0.8,
            lineJoin: 'round'
        }).addTo(window.map).bringToFront();

        map.fitBounds(window.routeLayer.getBounds());
    }

    function handleLocationClick() {
        if (!navigator.geolocation) {
            alert("Геолокация не поддерживается вашим браузером");
            return;
        }

        navigator.geolocation.getCurrentPosition(
            position => {
                const { latitude: lat, longitude: lng } = position.coords;
                fromInput.value = `${lat.toFixed(5)}, ${lng.toFixed(5)}`;

                // Добавляем маркер
                L.marker([lat, lng], { icon: icons.user })
                    .addTo(window.map)
                    .bindPopup("Ваше местоположение")
                    .openPopup();

                // Центрируем карту
                window.map.setView([lat, lng], 15);
            },
            error => alert("Ошибка геолокации: " + error.message)
        );
    }

    function handleRouteError(error) {
        console.error("Ошибка маршрута:", error);
        alert(`Ошибка: ${error || "Неизвестная ошибка"}`);
        if (window.routeLayer) window.map.removeLayer(window.routeLayer);
    }

    // Инициализация геолокации (если нужно)
    if (typeof initGeolocation === 'function') {
        initGeolocation();
    }
});