module.exports = {
  sendToWebhook,
};

/**
 * Fetches data from the specified URL.
 *
 * @param {string} url - The URL to fetch data from.
 * @param {string} stringified_json - the json data to send
 * @returns {Promise<Object>} The fetched data.
 */
function sendToWebhook(url, stringified_json) {
  fetch(url, {
    method: "POST",
    body: stringified_json,
    headers: {
      "Content-type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((json) => console.log(json));
}
