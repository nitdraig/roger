async function showSuggestions(input, suggestionsContainerId) {
  const query = input.value.trim();

  if (query.length === 0) {
    document.getElementById(suggestionsContainerId).innerHTML = "";
    return;
  }

  fetch(`/autocomplete_stocks?query=${query}`)
    .then((response) => response.json())
    .then((suggestions) => {
      const suggestionsContainer = document.getElementById(
        suggestionsContainerId
      );
      suggestionsContainer.innerHTML = "";

      suggestions.forEach((suggestion) => {
        const suggestionItem = document.createElement("div");
        suggestionItem.className = "suggestion-item";
        suggestionItem.textContent = `${suggestion.symbol} - ${suggestion.name}`;
        suggestionItem.onclick = function () {
          input.value = suggestion.symbol;
          suggestionsContainer.innerHTML = "";
        };
        suggestionsContainer.appendChild(suggestionItem);
      });
    });
}

async function compareStocks() {
  const ticker1 = document.getElementById("ticker-input-1").value.trim();
  const ticker2 = document.getElementById("ticker-input-2").value.trim();
  const spinner = document.getElementById("spinner");

  if (!ticker1 || !ticker2) {
    alert("Please enter both stock symbols.");
    return;
  }
  spinner.style.display = "block";

  fetch(`/compare_stocks?ticker1=${ticker1}&ticker2=${ticker2}`)
    .then((response) => response.json())
    .then((result) => {
      const resultContainer = document.getElementById("comparison-result");

      if (result.error) {
        resultContainer.innerHTML = `<p>${result.error}</p>`;
        return;
      }
      spinner.style.display = "none";
      resultContainer.innerHTML = `
        <h3>Comparison Result</h3>
        <p><strong>${result.stock1.ticker}</strong>: ${result.stock1.explanation}</p>
        <p><strong>${result.stock2.ticker}</strong>: ${result.stock2.explanation}</p>
        <p><strong>Recommendation</strong>: ${result.comparison_recommendation}</p>
        <p>${result.comparison_explanation}</p>
      `;
    })
    .catch((error) => {
      console.error("Error comparing stocks:", error);
    });
}
