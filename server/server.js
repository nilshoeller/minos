const express = require("express");
const path = require("path");

const app = express();
const PORT = 3000;
const CLOUD_FUNCS_URL = "http://localhost:8000";

app.use(express.json());

// Routing
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "/public/index.html"));
});

app.get("/about", (req, res) => {
  res.sendFile(path.join(__dirname, "/public/about.html"));
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
