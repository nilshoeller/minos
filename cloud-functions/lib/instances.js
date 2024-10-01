module.exports = {
  invokeNewInstance,
};

async function invokeNewInstance(req, res, url) {
  let retryCount = req.headers["retry-count"] || 0;

  if (retryCount >= 3) {
    return res.status(500).send({
      message: "Max retry-limit reached, computation failed.",
    });
    // process.exit(0);
  }

  try {
    const response = await fetch(url, {
      method: req.method,
      headers: {
        ...req.headers,
        "Content-Type": "application/json", // Ensure content type is set if sending JSON
        "retry-count": retryCount + 1,
      },
      body: req.method !== "GET" ? JSON.stringify(req.body) : undefined, // Only send body for non-GET requests
    });

    // ------
    const data = await response.json(); // Parse the response
    if (response.ok) {
      // Return the response from the new instance
      return res.status(200).send({
        message: `New instance invoked successfully. Retry count: ${retryCount}`,
        data: data,
      });
    } else {
      // Handle errors from the new instance
      return res.status(500).send({
        message: `Error from new instance (Retry count: ${retryCount}): ${data.message}`,
      });
    }
    // ------
  } catch (error) {
    return res.status(500).send({
      message: `Failed invoking new instance: ${error.message}`,
    });
  }
}
