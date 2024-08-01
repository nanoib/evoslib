(function() {
    function renderComponents(components) {
        const grid = document.getElementById('componentGrid');
        grid.innerHTML = '';

        components.forEach(component => {
            const tile = document.createElement('div');
            tile.className = 'component-tile';

            const img = document.createElement('img');
            img.src = `./im/${component.imageUrl}`;
            img.alt = component.name;

            const details = document.createElement('div');
            details.className = 'component-details';

            const grayInfo = document.createElement('p');
            grayInfo.className = 'gray-info';
            grayInfo.textContent = `${component.technicalCategory || ''}${component.surname ? ' ' + component.surname : ''}: ${component.manufacturer || ''}`.trim();
            grayInfo.style.color = 'gray';
            grayInfo.style.fontSize = '0.9em';

            const name = document.createElement('p');
            name.className = 'component-name';
            name.textContent = component.name;

            details.appendChild(grayInfo);
            details.appendChild(name);

            tile.appendChild(img);
            tile.appendChild(details);
            tile.addEventListener('click', () => openModal(component));

            grid.appendChild(tile);
        });
    }

    window.renderComponents = renderComponents;
})();