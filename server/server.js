const express = require("express");
const path = require("path");

const app = express();
const PORT = 3000;
const CLOUD_FUNCS_URL = "http://localhost:8000";

let latestWebhookData = null;

app.use(express.json());
app.use("/static", express.static("static"));

// Routing
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "/public/index.html"));
});

app.get("/about", (req, res) => {
  res.sendFile(path.join(__dirname, "/public/about.html"));
});

app.post("/webhook", (req, res) => {
  const payload = req.body;
  console.log("Webhook received:", payload);

  // You can process the payload here, e.g., save it to a database or trigger other actions
  latestWebhookData = payload;

  // Respond to acknowledge receipt of the webhook
  res.status(200).send({
    message: "Webhook received",
  });
});

// Endpoint to serve the latest webhook data
app.get("/latest-webhook", (req, res) => {
  res.status(200).json(latestWebhookData || { status: "No webhook data yet" });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
