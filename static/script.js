document.addEventListener('DOMContentLoaded', function() {
    let boardGames = []; // This will hold the data fetched from the backend
    let filteredGames = []; // This will hold the filtered data
    let debounceTimer; // Timer for debouncing

    // Fetch data from the backend
    fetch('/api/boardgames')
        .then(response => response.json())
        .then(data => {
            boardGames = data;
            filteredGames = data;
            populateCategories(data);
            renderTable(data);
        });

    // Function to populate categories in the filter dropdown
    function populateCategories(data) {
        let categories = new Set();
        data.forEach(game => {
            game.Category.forEach(category => categories.add(category));
        });
        let categoryFilter = document.getElementById('categoryFilter');
        categories.forEach(category => {
            let option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            categoryFilter.appendChild(option);
        });
    }

    // Function to render the table with the given data
    function renderTable(data) {
        let tableBody = document.querySelector('#boardGameTable tbody');
        tableBody.innerHTML = '';
        data.forEach(game => {
            let row = document.createElement('tr');
            row.innerHTML = `
                <td>${game.BoardGameName}</td>
                <td>${game.MinimumPlayers}</td>
                <td>${game.MaximumPlayers}</td>
                <td>${game.Category.join(', ')}</td>
                <td>${game.FirstLED}</td>
                <td>${game.LastLED}</td>
            `;
            tableBody.appendChild(row);
        });
    }

    // Function to apply filters and update the table
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
        debounceTimer = setTimeout(() => {
            sendSelectedRecords();
        }, 3000); // 3 seconds delay
    }

    // Function to send selected records to the backend
    function sendSelectedRecords() {
        let selectedRecords = filteredGames.map(game => {
            return {
                BoardGameName: game.BoardGameName,
                MinimumPlayers: game.MinimumPlayers,
                MaximumPlayers: game.MaximumPlayers,
                Category: game.Category,
                FirstLED: game.FirstLED,
                LastLED: game.LastLED
            };
        });

        fetch('/api/selected-games', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(selectedRecords)
        })
        .then(response => response.json())
        .then(data => {
            // No need for a popup confirmation, flash message is handled by Flask
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Apply filters when the button is clicked
    document.getElementById('applyFilters').addEventListener('click', applyFilters);

    // Apply filters when any filter input changes
    document.getElementById('nameFilter').addEventListener('input', applyFilters);
    document.getElementById('categoryFilter').addEventListener('change', applyFilters);
    document.getElementById('playersFilter').addEventListener('input', applyFilters);

    // Send selected records to the backend when the button is clicked
    document.getElementById('sendSelected').addEventListener('click', sendSelectedRecords);
});