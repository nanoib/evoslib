(function() {
    window.filters = {
        siteCategory: {},
        manufacturer: [],
        graphicType: [],
        shape: []
    };

    document.addEventListener('DOMContentLoaded', () => {
        fetch('./db/Base.json')
            .then(response => response.json())
            .then(data => {
                window.components = data;
                initializeFilters();
                const sortedComponents = sortComponents(components, 'updDate'); // Default sorting by name
                renderComponents(sortedComponents);
            })
            .catch(error => console.error('Error loading JSON data:', error));
    });
    
    // Add event listener for reset button
    document.getElementById('resetFilters').addEventListener('click', resetFilters);
    document.getElementById('resetFilters').style.display = 'none';
    document.getElementById('downloadSelected').addEventListener('click', downloadSelectedComponents);

    // Add event listener for sort select dropdown
    document.getElementById('sortSelect').addEventListener('change', (event) => {
        const currentFilters = getCurrentFilters(); // Assume this function exists and returns current filter state
        const filteredComponents = applyFilters(components, currentFilters); // Assume this function exists and applies filters
        const sortedComponents = sortComponents(filteredComponents, event.target.value);
        renderComponents(sortedComponents);
    });

    document.addEventListener('DOMContentLoaded', () => {
        const memoryUsageElement = document.getElementById('memoryUsage');
    
        function updateMemoryUsage() {
            if (performance.memory) {
                const memory = performance.memory;
                const usedMB = (memory.usedJSHeapSize / 1048576).toFixed(2);
                memoryUsageElement.textContent = `Потребление памяти: ${usedMB} Mb`;
            } else {
                memoryUsageElement.textContent = ' ';
            }
        }
    
        // Update memory usage every 5 seconds
        setInterval(updateMemoryUsage, 5000);
    
        // Initial call to display memory usage immediately
        updateMemoryUsage();
    });

})();