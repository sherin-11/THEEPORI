// script.js
document.addEventListener("DOMContentLoaded", function() {
    const dataList = document.getElementById("data-list");

    // Fetch data from your Flask API endpoint
    fetch('/api/endpoint') // Replace with your API endpoint
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const listItem = document.createElement("li");
                listItem.innerText = item.name; // Replace with your data structure
                dataList.appendChild(listItem);
            });
        })
        .catch(error => console.error(error));
});