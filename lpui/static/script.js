document.addEventListener('DOMContentLoaded', function() {
    const boardGameNameInput = document.getElementById('boardGameName');
    const categorySelect = document.getElementById('category');
    const minPlayersInput = document.getElementById('minPlayers');
    const maxPlayersInput = document.getElementById('maxPlayers');
    const clearFiltersButton = document.getElementById('clearFilters');
    const publishButton = document.getElementById('publish');
    const resultsDiv = document.getElementById('results');

    let boardGames = [];
    let filteredBoardGames = [];

    // Fetch data from the API
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            boardGames = data;
            filteredBoardGames = data;
            populateCategories(data);
            displayBoardGames(data);
        });

    // Populate categories in the multiselect
    function populateCategories(data) {
        const categories = new Set();
        data.forEach(game => {
            game.categories.forEach(category => {
                categories.add(category.category_name);
            });
        });
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            categorySelect.appendChild(option);
        });
    }

    // Display board games
    function displayBoardGames(games) {
        resultsDiv.innerHTML = '';
        games.forEach(game => {
            const gameDiv = document.createElement('div');
            gameDiv.textContent = game.board_game_name;
            resultsDiv.appendChild(gameDiv);
        });
    }

    // Filter board games based on user input
    function filterBoardGames() {
        const boardGameName = boardGameNameInput.value.toLowerCase();
        const selectedCategories = Array.from(categorySelect.selectedOptions).map(option => option.value);
        const minPlayers = parseInt(minPlayersInput.value) || 0;
        const maxPlayers = parseInt(maxPlayersInput.value) || Infinity;

        filteredBoardGames = boardGames.filter(game => {
            const nameMatch = game.board_game_name.toLowerCase().includes(boardGameName);
            const categoryMatch = selectedCategories.length === 0 || game.categories.some(category => selectedCategories.includes(category.category_name));
            const playerMatch = game.minimum_players >= minPlayers && game.maximum_players <= maxPlayers;
            return nameMatch && categoryMatch && playerMatch;
        });

        displayBoardGames(filteredBoardGames);
    }

    // Clear all filters
    clearFiltersButton.addEventListener('click', function() {
        boardGameNameInput.value = '';
        categorySelect.selectedIndex = -1;
        minPlayersInput.value = '';
        maxPlayersInput.value = '';
        filteredBoardGames = boardGames;
        displayBoardGames(boardGames);
    });

    // Publish filtered board game IDs
    publishButton.addEventListener('click', function() {
        const boardGameIds = filteredBoardGames.map(game => game.id);
        console.log(boardGameIds);
        fetch('/publish', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ board_game_ids: boardGameIds })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Publish response:', data);
        });
    });

    // Add event listeners to filter inputs
    boardGameNameInput.addEventListener('input', filterBoardGames);
    categorySelect.addEventListener('change', filterBoardGames);
    minPlayersInput.addEventListener('input', filterBoardGames);
    maxPlayersInput.addEventListener('input', filterBoardGames);
});