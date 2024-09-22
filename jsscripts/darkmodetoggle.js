document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const lightStylesheets = document.querySelectorAll('link[href^="styles/light/"]');
    const darkStylesheets = document.querySelectorAll('link[href^="styles/dark/"]');

    // Function to toggle between light and dark mode
    function toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
        lightStylesheets.forEach(sheet => sheet.disabled = !sheet.disabled);
        darkStylesheets.forEach(sheet => sheet.disabled = !sheet.disabled);
        
        // Save the current mode to localStorage
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
    }

    // Check for saved user preference
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode === 'true') {
        document.body.classList.add('dark-mode');
        lightStylesheets.forEach(sheet => sheet.disabled = true);
        darkStylesheets.forEach(sheet => sheet.disabled = false);
    } else {
        lightStylesheets.forEach(sheet => sheet.disabled = false);
        darkStylesheets.forEach(sheet => sheet.disabled = true);
    }

    // Add click event listener to the toggle button
    darkModeToggle.addEventListener('click', toggleDarkMode);

    // Set the initial value of window.isDarkMode
    window.isDarkMode = document.body.classList.contains('dark-mode');

    // Update window.isDarkMode whenever the mode changes
    function updateIsDarkMode() {
        window.isDarkMode = document.body.classList.contains('dark-mode');
    }

    // Add updateIsDarkMode to the existing toggleDarkMode function
    const originalToggleDarkMode = toggleDarkMode;
    toggleDarkMode = function() {
        originalToggleDarkMode();
        updateIsDarkMode();
    };

    // Call updateIsDarkMode initially to set the correct value
    updateIsDarkMode();

    // Reload the page when dark mode is toggled
    darkModeToggle.addEventListener('click', () => {
        setTimeout(() => {
            window.location.reload();
        }, 100);
    });

});

