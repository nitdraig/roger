function compareStocks() {
  const ticker1 = document.getElementById("ticker-input-1").value.trim();
  const ticker2 = document.getElementById("ticker-input-2").value.trim();

  if (!ticker1 || !ticker2) {
    alert("Please enter both action symbols.");
    return;
  }

  fetch(`/compare_stocks?ticker1=${ticker1}&ticker2=${ticker2}`)
    .then((response) => response.json())
    .then((data) => {
      const resultDiv = document.getElementById("comparison-result");
      if (data.error) {
        resultDiv.innerHTML = `<p class="error">${data.error}</p>`;
      } else {
        resultDiv.innerHTML = `
            <h3>Comparison between ${ticker1} & ${ticker2}</h3>
            <p><strong>${ticker1}:</strong> Performance: ${data.stock1.performance}, Current Value: ${data.stock1.current_value}</p>
            <p><strong>${ticker2}:</strong> Performance: ${data.stock2.performance}, Current Value: ${data.stock2.current_value}</p>
          `;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
