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
                renderComponents(components);
            })
            .catch(error => console.error('Error loading JSON data:', error));
    });
    
    // Add event listener for reset button
    document.getElementById('resetFilters').addEventListener('click', resetFilters);
    document.getElementById('resetFilters').style.display = 'none';

})();