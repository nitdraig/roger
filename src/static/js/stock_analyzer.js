let debounceTimer;

async function fetchSuggestions() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(async () => {
    const query = document.getElementById("ticker-input").value.trim();
    const suggestionsDiv = document.getElementById("suggestions");

    if (!query) {
      suggestionsDiv.innerHTML = "";
      return;
    }

    try {
      const response = await fetch(`/autocomplete?query=${query}`);
      if (!response.ok) throw new Error("Network response was not ok");

      const suggestions = await response.json();
      suggestionsDiv.innerHTML = "";

      suggestions.forEach((suggestion) => {
        const suggestionItem = document.createElement("div");
        suggestionItem.textContent = `${suggestion.name} (${suggestion.symbol})`;
        suggestionItem.classList.add("suggestion-item");
        suggestionItem.onclick = () => selectSuggestion(suggestion);
        suggestionsDiv.appendChild(suggestionItem);
      });
    } catch (error) {
      console.error("Fetch suggestions failed:", error);
      suggestionsDiv.innerHTML = "";
    }
  }, 300);
}

function selectSuggestion(suggestion) {
  document.getElementById("ticker-input").value = suggestion.symbol;
  document.getElementById("suggestions").innerHTML = "";
}

async function analyzeStock() {
  const ticker = document.getElementById("ticker-input").value.trim();
  const resultDiv = document.getElementById("result");
  const spinner = document.getElementById("spinner");

  if (!ticker) {
    resultDiv.innerHTML = "<p>Please enter a valid stock symbol.</p>";
    return;
  }

  spinner.style.display = "block";
  resultDiv.innerHTML = "";

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ticker: ticker }),
    });

    const result = await response.json();

    spinner.style.display = "none";

    if (response.ok) {
      resultDiv.innerHTML = `<h2>${result.ticker}</h2>
            <p>Recommendation: ${result.recommendation}</p>
            <p>Sharpe Ratio: ${result.sharpe_ratio.toFixed(2)}</p>
            <p>Explanation: ${result.explanation}</p>`;
    } else {
      resultDiv.innerHTML = `<p>Error: ${result.error}</p>`;
    }
  } catch (error) {
    spinner.style.display = "none";
    resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
  }
}
