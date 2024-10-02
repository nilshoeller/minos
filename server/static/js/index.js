function callCloudFunction() {
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

document.addEventListener("DOMContentLoaded", () => {
  // Function to fetch and update webhook data
  async function fetchWebhookData() {
    try {
      const response = await fetch("/latest-webhook");
      const data = await response.json();

      // Update the HTML to display the received data
      document.getElementById("webhook-data").innerHTML = `
          <p>Status: ${data.status}</p>
          <p>Completed: ${data.completed || "N/A"}</p>
        `;
    } catch (error) {
      console.error("Error fetching webhook data:", error);
    }
  }

  // Poll the server every 5 seconds to get the latest webhook data
  setInterval(fetchWebhookData, 5000);
});
