(function() {
    function renderComponents(components) {
        const grid = document.getElementById('componentGrid');
        grid.innerHTML = '';

        components.forEach(component => {
            const tile = document.createElement('div');
            tile.className = 'component-tile';

            const img = document.createElement('img');
            img.src = `./im/${component.id}.png`;
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
            tile.setAttribute('data-component-id', component.id);
        });
    }

    function sortComponents(components, sortBy) {
        return components.sort((a, b) => {
            if (sortBy === 'name') {
                return a.name.localeCompare(b.name);
            } else if (sortBy === 'manufacturer') {
                return a.manufacturer.localeCompare(b.manufacturer);
            } else if (sortBy === 'updDate') {
                return new Date(b.updDate) - new Date(a.updDate);
            } else if (sortBy === 'technicalCategory') {
                if (a.siteCategory === b.siteCategory) {
                    return a.technicalCategory.localeCompare(b.technicalCategory);
                }
                return a.siteCategory.localeCompare(b.siteCategory);
            }
        });
    }

    document.getElementById('sortSelect').addEventListener('change', (event) => {
        const sortedComponents = sortComponents(components, event.target.value);
        renderComponents(sortedComponents);
    });

    function downloadSelectedComponents() {
        const renderedComponents = document.querySelectorAll('.component-tile');
        if (renderedComponents.length === 0) {
            console.log('No components to download');
            alert('Нет компонентов для скачивания.');
            return;
        }
    
        console.log(`Found ${renderedComponents.length} components to download`);
    
        const zip = new JSZip();
        const sizeLimit = 50 * 1024 * 1024; // 50 MB limit
        let totalSize = 0;
    
        const calculateSize = (url) => {
            return fetch(url, { method: 'HEAD' })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return parseInt(response.headers.get('content-length') || '0');
                });
        };
    
        const sizePromises = Array.from(renderedComponents).map(tile => {
            const componentId = tile.getAttribute('data-component-id');
            const component = window.components.find(c => String(c.id) === String(componentId));
            
            if (component) {
                const zipFileName = `id${component.id}_v${component.version}_${component.name}.zip`;
                const zipFilePath = `./components/${component.siteCategory}/${component.technicalCategory}/id${component.id}_v${component.version}_${component.name}/${zipFileName}`;
                return calculateSize(zipFilePath);
            }
            return Promise.resolve(0);
        });
    
        Promise.all(sizePromises)
            .then(sizes => {
                totalSize = sizes.reduce((acc, size) => acc + size, 0);
                console.log(`Total size to download: ${totalSize} bytes`);
    
                if (totalSize > sizeLimit) {
                    alert('Пожалуйста, подождите! Ваш архив больше 50 Мб. Создание архива может занять несколько минут. Скачивание начнется автоматически');
                }
    
                const addFileToZip = (url, filename, siteCategory) => {
                    console.log(`Attempting to fetch: ${url}`);
                    return fetch(url)
                        .then(response => {
                            if (!response.ok) {
                                throw new Error(`HTTP error! status: ${response.status}`);
                            }
                            console.log(`Fetch successful for ${filename}`);
                            return response.blob();
                        })
                        .then(blob => {
                            console.log(`Adding ${filename} to zip. Blob size: ${blob.size} bytes`);
                            zip.folder(siteCategory).file(filename, blob);
                            console.log(`Added ${filename} to zip in folder ${siteCategory}`);
                        })
                        .catch(error => {
                            console.error(`Failed to add ${filename}: ${error}`);
                        });
                };
    
                const promises = Array.from(renderedComponents).map(tile => {
                    const componentId = tile.getAttribute('data-component-id');
                    const component = window.components.find(c => String(c.id) === String(componentId));
                    
                    if (component) {
                        const zipFileName = `id${component.id}_v${component.version}_${component.name}.zip`;
                        const zipFilePath = `./components/${component.siteCategory}/${component.technicalCategory}/id${component.id}_v${component.version}_${component.name}/${zipFileName}`;
                        
                        return addFileToZip(zipFilePath, zipFileName, component.siteCategory);
                    } else {
                        console.warn(`Component not found for ID: ${componentId}`);
                        return Promise.resolve();
                    }
                });
    
                return Promise.all(promises);
            })
            .then(() => {
                console.log('All files processed. Generating final zip...');
                return zip.generateAsync({type:"blob"});
            })
            .then(content => {
                console.log(`Final zip size: ${content.size} bytes`);
                console.log('Zip contents:');
                zip.forEach((relativePath, zipEntry) => {
                    console.log(`- ${relativePath}: ${zipEntry.uncompressedSize} bytes`);
                });
    
                const url = window.URL.createObjectURL(content);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = 'selected_components.zip';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                console.log('Download initiated');
            })
            .catch(error => {
                console.error('Error during download process:', error);
                alert('Произошла ошибка при загрузке файлов. Пожалуйста, попробуйте еще раз.');
            });
    }
    
    window.sortComponents = sortComponents;
    window.renderComponents = renderComponents;
    window.downloadSelectedComponents = downloadSelectedComponents;

})();