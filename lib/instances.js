module.exports = {
  invokeNewInstance,
};

async function invokeNewInstance(req) {
  const retryCount = req.headers["x-retry-count"] || 0;

  if (retryCount >= 3) {
    console.log("Max retry limit reached.");
    return {
      status: 500,
      message: "Max retry limit reached, computation failed.",
    };
  }

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-retry-count": parseInt(retryCount) + 1, // Increment retry count
      },
    });

    if (!response.ok) {
      let errorMessage = `HTTP error! Status: ${response.status}`;

      try {
        const errorData = await response.json();
        errorMessage = errorData.message || errorMessage;
      } catch (parseError) {
        console.error("Failed to parse error response:", parseError);
      }

      return {
        status: response.status,
        message: errorMessage,
      };
    }

    let data = await response.json();
    return {
      status: data.status,
      message: data.message || "Success",
    };
  } catch (error) {
    console.error("Error:", error);
    return {
      status: 500,
      message: "Failed invoking new instance: " + error.message,
    };
  }
}
