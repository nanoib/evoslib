(function() {
    function openModal(component) {
        const modal = document.getElementById('modal');
        const modalImage = document.getElementById('modal-image');
        const modalText = document.getElementById('modal-text');

        modalImage.src = `./im/${component.id}.png`;
        modalImage.alt = component.name;

        let modalContent = '';

        // Generate the download link
        const downloadLink = `./components/${component.siteCategory}/${component.technicalCategory}/id${component.id}_v${component.version}_${component.name}/id${component.id}_v${component.version}_${component.name}.zip`;

        if (component.siteCategory) {
            modalContent += `<p style="display: flex; justify-content: space-between; align-items: center;">
                                <strong>Категория:</strong> <span>${component.siteCategory}</span>
                                <a href="${downloadLink}" class="download-button" download style="margin-left: auto;">Скачать</a>
                             </p>`;
        }
        
        if (component.technicalCategory) {
            modalContent += `<p><strong>Подкатегория:</strong> <span>${component.technicalCategory}</span></p>`;
        }

        if (component.surname) {
            modalContent += `<p><strong>Дополнительная характеристика:</strong> <span>${component.surname}</span></p>`;
        }

        if (component.note) {
            modalContent += `<p><strong>Описание:</strong> <span>${component.note}</span></p>`;
        }

        if (component.graphicType && component.graphicType !== "Не применимо") {
            modalContent += `<p><strong>Тип графики:</strong> <span>${component.graphicType}</span></p>`;
        }

        if (component.shape && component.shape !== "Не применимо") {
            modalContent += `<p><strong>Форма:</strong> <span>${component.shape}</span></p>`;
        }

        if (component.typesizes) {
            const typesizesArray = component.typesizes.split(';').map(size => size.trim());
            const formattedTypesizes = typesizesArray.join(';<br>');
            const typesizesTitle = component.graphicType === "Параметрическая" 
                ? 'Доступные типоразмеры <i><span class="info-icon" title="Этот компонент с параметрической графикой.\nЭто значит, что вы легко можете добавить новые типоразмеры копированием\nкомпонента и дальнейшей заменой значений параметров">i</span></i>:'
                : 'Доступные типоразмеры:';
            modalContent += `<p><strong>${typesizesTitle}</strong><br><span>${formattedTypesizes}</span></p>`;
        }

        if (component.manufUrl) {
            modalContent += `<p id="modal-link"><strong>Ссылка на сайт производителя:</strong> <span><a href="${component.manufUrl}" target="_blank">${component.manufUrl}</a></span></p>`;
        }

        if (component.versionHistory) {
            const versionHistoryArray = component.versionHistory.split(';').map(version => {
                return version.replace(/(v\d+)/g, '<strong>$1</strong>').trim();
            });
            const formattedVersionHistory = versionHistoryArray.join(';<br>');
            modalContent += `<p><strong>История версий:</strong><br><span>${formattedVersionHistory}</span></p>`;
        }

        if (component.id) {
            modalContent += `<p><strong>ID в библиотеке:</strong> <span>${component.id}</span></p>`;
        }
        
        if (component.updDate) {
            const date = new Date(component.updDate);
            const formattedDate = date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
            modalContent += `<p><strong>Дата последнего обновления:</strong> <span>${formattedDate}</span></p>`;
        }
    

        modalText.innerHTML = `<hr>${modalContent}`;

        modal.style.display = 'flex';
        modalImage.addEventListener('click', closeModal);
        document.addEventListener('keydown', handleKeyDown);
        modal.addEventListener('click', handleOutsideClick);
    }

    function closeModal() {
        const modal = document.getElementById('modal');
        modal.style.display = 'none';
        const modalImage = document.getElementById('modal-image');
        modalImage.removeEventListener('click', closeModal);
        document.removeEventListener('keydown', handleKeyDown);
        modal.removeEventListener('click', handleOutsideClick);
    }

    function handleKeyDown(event) {
        if (event.key === 'Escape') {
            closeModal();
        }
    }

    function handleOutsideClick(event) {
        const modalContent = document.querySelector('.modal-content');
        if (!modalContent.contains(event.target)) {
            closeModal();
        }
    }

    function initializeModal() {
        const modal = document.getElementById('modal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    window.openModal = openModal;
    window.closeModal = closeModal;
    window.initializeModal = initializeModal;

    document.addEventListener('DOMContentLoaded', () => {
        initializeModal();
    });
})();