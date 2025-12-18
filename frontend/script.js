console.log("Script loaded");

document.getElementById("checkBtn").addEventListener("click", checkSpam);

function checkSpam() {
  console.log("Button clicked");

  const msg = document.getElementById("message").value;
  const resultBox = document.getElementById("resultBox");
  const resultText = document.getElementById("resultText");
  const confidenceText = document.getElementById("confidenceText");

  if (!msg.trim()) {
    alert("Please enter a message");
    return;
  }

  resultBox.classList.remove("hidden");
  resultText.innerText = "Checking...";
  confidenceText.innerText = "";

  fetch("https://spam-classifier-j3al.onrender.com/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: msg })
  })
    .then(res => {
      console.log("Response received");
      return res.json();
    })
    .then(data => {
      console.log("API data:", data);

      resultText.innerText = data.prediction;
      resultText.style.color =
        data.prediction === "Spam" ? "red" : "green";

      confidenceText.innerText =
        `Confidence: ${Math.round(data.confidence * 100)}%`;
    })
    .catch(err => {
      console.error("Fetch error:", err);
      resultText.innerText = "Server error";
    });
}


