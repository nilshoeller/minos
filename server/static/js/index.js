function callCloudFunction() {
  console.log("Sending request to cloud function.");

  fetch("http://localhost:8080/", {
    method: "GET",
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json(); // Assuming the response is JSON
    })
    .then((data) => {
      console.log("Success:", data); // Process the response data
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
}

async function fetchData() {
  const response = await fetch("/webhook-data");
  const dataList = await response.json();
  const listElement = document.getElementById("webhook-data-list");
  listElement.innerHTML = ""; // Clear the list before appending

  dataList.forEach((data) => {
    const listItem = document.createElement("li");
    listItem.textContent = `Status: ${data.status}, Message: ${data.message}`;

    // JSON.stringify(data); // Adjust according to your data structure
    listElement.appendChild(listItem);
  });
}
// Initial call to fetch data
fetchData();
// Fetch data every 5 seconds
setInterval(fetchData, 2500);
