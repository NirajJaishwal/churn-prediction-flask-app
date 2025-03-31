function goBack() {
    window.history.back();
}
function nextPrediction() {
    sessionStorage.clear();
    window.location.href = "/";
}
window.onload = function() {
    let resultText = document.getElementById("prediction_text");
    if (resultText.innerText.includes("Not Churn")) {
        resultText.style.color = "green";
    } else {
        resultText.style.color = "red";
    }
};