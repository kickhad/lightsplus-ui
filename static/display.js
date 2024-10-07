document.addEventListener('DOMContentLoaded', function() {
    const ledDisplay = document.getElementById('ledDisplay');

    // Generate the initial row of 100 black squares
    for (let i = 1; i <= 100; i++) {
        let square = document.createElement('div');
        square.className = 'led-square bg-dark';
        ledDisplay.appendChild(square);
    }

    // Function to update the LED display based on the received data
    function updateLEDDisplay(ledIndices) {
        const squares = document.querySelectorAll('.led-square');
        squares.forEach((square, index) => {
            if (ledIndices.includes(index + 1)) {
                square.classList.remove('bg-dark');
                square.classList.add('bg-primary');
            } else {
                square.classList.remove('bg-primary');
                square.classList.add('bg-dark');
            }
        });
    }

    // Fetch the initial LED data from the backend
    function fetchLEDData() {
        fetch('/api/led-data')
            .then(response => response.json())
            .then(data => {
                updateLEDDisplay(data.ledIndices);
            });
    }

    // Periodically refresh the LED display
    setInterval(fetchLEDData, 5000);  // Refresh every 5 seconds

    // Fetch the initial LED data
    fetchLEDData();
});