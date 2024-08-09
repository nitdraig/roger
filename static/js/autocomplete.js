document.addEventListener('DOMContentLoaded', function() {
    const stockInput = document.getElementById('stock-input');
    const suggestionBox = document.getElementById('suggestions');

    stockInput.addEventListener('input', function() {
        const query = stockInput.value;

        if (query.length > 1) {
            fetch(`/autocomplete?query=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestionBox.innerHTML = '';
                    data.forEach(stock => {
                        const div = document.createElement('div');
                        div.textContent = `${stock.symbol} - ${stock.name}`;
                        div.addEventListener('click', () => {
                            stockInput.value = stock.symbol;
                            suggestionBox.innerHTML = '';
                        });
                        suggestionBox.appendChild(div);
                    });
                });
        } else {
            suggestionBox.innerHTML = '';
        }
    });
});
