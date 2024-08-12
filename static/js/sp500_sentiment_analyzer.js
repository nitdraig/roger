// static/js/sp500_sentiment_analyzer.js
function fetchSentiment() {
  fetch("/sp500_sentiment")
    .then((response) => response.json())
    .then((data) => {
      const resultDiv = document.getElementById("result");
      if (data.error) {
        resultDiv.innerHTML = `<p class="error">${data.error}</p>`;
      } else {
        resultDiv.innerHTML = `
            <p><strong>Average Sentiment Score:</strong> ${data.average_sentiment}</p>
            <p><strong>Sentiment:</strong> ${data.sentiment}</p>
            <p><strong>Total Articles:</strong> ${data.total_articles}</p>
          `;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
