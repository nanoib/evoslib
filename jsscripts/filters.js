(function() {
    function initializeFilters() {
        const siteCategoryMapping = {};
        const technicalCategoryMapping = {};

        components.forEach(component => {
            if (component.siteCategory && component.technicalCategory) {
                if (!siteCategoryMapping[component.siteCategory]) {
                    siteCategoryMapping[component.siteCategory] = new Set();
                }
                siteCategoryMapping[component.siteCategory].add(component.technicalCategory);

                if (!technicalCategoryMapping[component.technicalCategory]) {
                    technicalCategoryMapping[component.technicalCategory] = component.siteCategory;
                }
            }
        });

        filters.siteCategory = Object.keys(siteCategoryMapping).reduce((acc, category) => {
            acc[category] = {
                checked: false,
                subcategories: Array.from(siteCategoryMapping[category]).reduce((subAcc, subCategory) => {
                    subAcc[subCategory] = false;
                    return subAcc;
                }, {})
            };
            return acc;
        }, {});

        filters.manufacturer = getUniqueValues(components, 'manufacturer');
        filters.graphicType = getUniqueValues(components, 'graphicType');
        filters.shape = getUniqueValues(components, 'shape');

        renderFilterOptions();
        applyFilters();
        resetFilters();
    }

    function getUniqueValues(array, key) {
        return [...new Set(array.map(item => item[key]).filter(Boolean))];
    }

    function renderFilterOptions() {
        renderCategoryFilters('siteCategory');
        renderSimpleFilters('manufacturer');
        renderSimpleFilters('graphicType');
        renderSimpleFilters('shape');
    }

    function renderCategoryFilters(filterType) {
        const container = document.getElementById(filterType);
        container.innerHTML = '';

        Object.entries(filters[filterType]).forEach(([category, data]) => {
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'filter-category';

            const categoryCheckbox = document.createElement('input');
            categoryCheckbox.type = 'checkbox';
            categoryCheckbox.id = `${filterType}-${category}`;
            categoryCheckbox.checked = data.checked;
            categoryCheckbox.addEventListener('change', () => handleCategoryChange(filterType, category));

            const categoryLabel = document.createElement('label');
            categoryLabel.htmlFor = categoryCheckbox.id;
            categoryLabel.textContent = category;

            categoryDiv.appendChild(categoryCheckbox);
            categoryDiv.appendChild(categoryLabel);

            container.appendChild(categoryDiv);

            Object.entries(data.subcategories).forEach(([subcategory, checked]) => {
                const subcategoryDiv = document.createElement('div');
                subcategoryDiv.className = 'filter-subcategory';

                const subCheckbox = document.createElement('input');
                subCheckbox.type = 'checkbox';
                subCheckbox.id = `${filterType}-${category}-${subcategory}`;
                subCheckbox.checked = checked;
                subCheckbox.addEventListener('change', () => handleSubcategoryChange(filterType, category, subcategory));

                const subLabel = document.createElement('label');
                subLabel.htmlFor = subCheckbox.id;
                subLabel.textContent = subcategory;

                subcategoryDiv.appendChild(subCheckbox);
                subcategoryDiv.appendChild(subLabel);

                container.appendChild(subcategoryDiv);
            });
        });
    }

    function renderSimpleFilters(filterType) {
        const container = document.getElementById(filterType);
        container.innerHTML = '';

        filters[filterType].forEach(value => {
            const filterDiv = document.createElement('div');
            filterDiv.className = 'filter-option';

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = `${filterType}-${value}`;
            checkbox.checked = false; // Ensure checkboxes are unchecked by default
            checkbox.addEventListener('change', () => handleFilterChange(filterType, value));

            const label = document.createElement('label');
            label.htmlFor = checkbox.id;
            label.textContent = value;

            filterDiv.appendChild(checkbox);
            filterDiv.appendChild(label);

            container.appendChild(filterDiv);
        });
    }

    function handleCategoryChange(filterType, category) {
        const isChecked = document.getElementById(`${filterType}-${category}`).checked;
        filters[filterType][category].checked = isChecked;

        Object.keys(filters[filterType][category].subcategories).forEach(subcategory => {
            filters[filterType][category].subcategories[subcategory] = isChecked;
            document.getElementById(`${filterType}-${category}-${subcategory}`).checked = isChecked;
        });

        applyFilters();
    }

    function handleSubcategoryChange(filterType, category, subcategory) {
        const isChecked = document.getElementById(`${filterType}-${category}-${subcategory}`).checked;
        filters[filterType][category].subcategories[subcategory] = isChecked;

        const allSubcategoriesChecked = Object.values(filters[filterType][category].subcategories).every(Boolean);
        filters[filterType][category].checked = allSubcategoriesChecked;
        document.getElementById(`${filterType}-${category}`).checked = allSubcategoriesChecked;

        applyFilters();
    }

    function handleFilterChange(filterType, value) {
        const isChecked = document.getElementById(`${filterType}-${value}`).checked;
        if (isChecked) {
            if (!filters[filterType].includes(value)) {
                filters[filterType].push(value);
            }
        } else {
            filters[filterType] = filters[filterType].filter(item => item !== value);
        }

        applyFilters();
    }

    function applyFilters() {
        const anyFilterSelected = Object.values(filters).some(f => 
            Array.isArray(f) ? f.length > 0 : Object.values(f).some(v => v.checked || Object.values(v.subcategories).some(Boolean))
        );

        const filteredComponents = anyFilterSelected ? components.filter(component => {
            const siteCategoryMatch = 
                Object.values(filters.siteCategory).some(category => 
                    category.checked || Object.values(category.subcategories).some(Boolean)
                ) ? (
                    filters.siteCategory[component.siteCategory]?.checked ||
                    filters.siteCategory[component.siteCategory]?.subcategories[component.technicalCategory]
                ) : true;

            const manufacturerMatch = 
                filters.manufacturer.length === 0 || 
                filters.manufacturer.includes(component.manufacturer);

            const graphicTypeMatch = 
                filters.graphicType.length === 0 || 
                filters.graphicType.includes(component.graphicType);

            const shapeMatch = 
                filters.shape.length === 0 || 
                filters.shape.includes(component.shape);

            return siteCategoryMatch && manufacturerMatch && graphicTypeMatch && shapeMatch;
        }) : components;

        renderComponents(filteredComponents);

        const resetButton = document.getElementById('resetFilters');
        resetButton.style.display = anyFilterSelected ? 'inline-block' : 'none';
    }

    function resetFilters() {
        Object.keys(filters).forEach(filterType => {
            if (Array.isArray(filters[filterType])) {
                filters[filterType] = [];
            } else {
                Object.keys(filters[filterType]).forEach(category => {
                    filters[filterType][category].checked = false;
                    Object.keys(filters[filterType][category].subcategories).forEach(subcategory => {
                        filters[filterType][category].subcategories[subcategory] = false;
                    });
                });
            }
        });
        
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });
    
        applyFilters();
    }

    window.initializeFilters = initializeFilters;
    window.getUniqueValues = getUniqueValues;
    window.renderFilterOptions = renderFilterOptions;
    window.renderCategoryFilters = renderCategoryFilters;
    window.renderSimpleFilters = renderSimpleFilters;
    window.handleCategoryChange = handleCategoryChange;
    window.handleSubcategoryChange = handleSubcategoryChange;
    window.handleFilterChange = handleFilterChange;
    window.applyFilters = applyFilters;
    window.resetFilters = resetFilters;
})();