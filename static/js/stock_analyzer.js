async function fetchSuggestions() {
    const query = document.getElementById("ticker-input").value;
    const response = await fetch(`/autocomplete?query=${query}`);
    const suggestions = await response.json();
    const suggestionsDiv = document.getElementById("suggestions");
    suggestionsDiv.innerHTML = "";

    suggestions.forEach((suggestion) => {
        const suggestionItem = document.createElement("div");
        suggestionItem.textContent = `${suggestion.name} (${suggestion.symbol})`;
        suggestionItem.onclick = () => selectSuggestion(suggestion);
        suggestionsDiv.appendChild(suggestionItem);
    });
}

function selectSuggestion(suggestion) {
    document.getElementById("ticker-input").value = suggestion.symbol;
    document.getElementById("suggestions").innerHTML = "";
}

async function analyzeStock() {
    const ticker = document.getElementById("ticker-input").value.toUpperCase();
    const response = await fetch("/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ ticker }),
    });
    const result = await response.json();
    if (result.error) {
        document.getElementById("result").innerHTML = `<p>${result.error}</p>`;
    } else {
        document.getElementById("result").innerHTML = `
            <h2>${result.ticker}</h2>
            <p>Recommendation: ${result.recommendation}</p>
            <p>Sharpe Ratio: ${result.sharpe_ratio.toFixed(2)}</p>
            <p>Explanation: ${result.explanation}</p>
        `;
    }
}
