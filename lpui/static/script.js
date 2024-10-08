document.addEventListener('DOMContentLoaded', function() {
    let boardGames = [];
    let filteredGames = [];
    let debounceTimer;

    // Fetch data from the backend
    fetch('/api/boardgames')
        .then(response => response.json())
        .then(data => {
            boardGames = data;
            filteredGames = data;
            populateCategories(data);
            renderTable(data);
        });

    // Populate categories in the filter dropdown
    function populateCategories(data) {
        let categories = new Set(data.flatMap(game => game.Category));
        let categoryFilter = document.getElementById('categoryFilter');
        categories.forEach(category => {
            categoryFilter.appendChild(new Option(category, category));
        });
    }

    // Render the table with the given data
    function renderTable(data) {
        let tableBody = document.querySelector('#boardGameTable tbody');
        tableBody.innerHTML = data.map(game => `
            <tr>
                <td>${game.BoardGameName}</td>
                <td>${game.MinimumPlayers}</td>
                <td>${game.MaximumPlayers}</td>
                <td>${game.Category.join(', ')}</td>
                <td>${game.FirstLED}</td>
                <td>${game.LastLED}</td>
            </tr>
        `).join('');
    }

    // Apply filters and update the table
    function applyFilters() {
        let nameFilter = document.getElementById('nameFilter').value.toLowerCase();
        let categoryFilter = Array.from(document.getElementById('categoryFilter').selectedOptions).map(option => option.value);
        let playersFilter = parseInt(document.getElementById('playersFilter').value);

        filteredGames = boardGames.filter(game => {
            let nameMatch = game.BoardGameName.toLowerCase().includes(nameFilter);
            let categoryMatch = categoryFilter.length === 0 || game.Category.some(category => categoryFilter.includes(category));
            let playersMatch = isNaN(playersFilter) || (game.MinimumPlayers <= playersFilter && game.MaximumPlayers >= playersFilter);
            return nameMatch && categoryMatch && playersMatch;
        });

        renderTable(filteredGames);
        debounceSendSelected();
    }

    // Debounce function to delay sending selected records
    function debounceSendSelected() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(sendSelectedRecords, 3000);
    }

    // Send selected records to the backend
    function sendSelectedRecords() {
        let numbersBetween = [];
        let selectedRecords = filteredGames.map(game => {
            for (let i = game.FirstLED; i <= game.LastLED; i++) {
                numbersBetween.push(i);
            }
            return {
                FirstLED: game.FirstLED,
                LastLED: game.LastLED,
                NumbersBetween: numbersBetween
            };
        });
    
        fetch('/api/selected-games', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(numbersBetween)
        })
        .then(response => response.json())
        .catch(console.error);
    }

    // Clear filters and reset the table
    function clearFilters() {
        document.getElementById('nameFilter').value = '';
        document.getElementById('categoryFilter').selectedIndex = -1;
        document.getElementById('playersFilter').value = '';
        filteredGames = boardGames;
        renderTable(boardGames);
        debounceSendSelected();
    }

    // Event listeners
    document.getElementById('applyFilters').addEventListener('click', applyFilters);
    document.getElementById('clearFilters').addEventListener('click', clearFilters);
    document.getElementById('nameFilter').addEventListener('input', applyFilters);
    document.getElementById('categoryFilter').addEventListener('change', applyFilters);
    document.getElementById('playersFilter').addEventListener('input', applyFilters);
    document.getElementById('sendSelected').addEventListener('click', sendSelectedRecords);
});