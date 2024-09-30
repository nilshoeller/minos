module.exports = {
  invokeNewInstance,
};

async function invokeNewInstance(req, res, url) {
  let retryCount = req.headers["retry-count"] || 0;

  if (retryCount >= 3) {
    return res.status(500).send({
      status: "500",
      message: "Max retry-limit reached, computation failed.",
    });
    // process.exit(0);
  }

  try {
    await fetch(url, {
      method: req.method,
      headers: {
        ...req.headers,
        "Content-Type": "application/json", // Ensure content type is set if sending JSON
        "retry-count": retryCount + 1,
      },
      body: req.method !== "GET" ? JSON.stringify(req.body) : undefined, // Only send body for non-GET requests
    });

    console.log("Invoked new instance.");
  } catch (error) {
    return res.status(500).send({
      message: `Failed invoking new instance: ${error.message}`,
    });
  }
}
