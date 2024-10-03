module.exports = {
  invokeNew,
};

/**
 * Re-invokes the function at the specified URL.
 *
 * @param {string} url - The URL to re-invoke the function.
 * @param {string} taskId - The ID of the current task.
 * @param {number} retryCount - The current retry attempt count.
 * @param {number} totalTimeOfExecution - The cumulative execution time across retries.
 * @param {number} timeOfExecution - The time taken by the current instance.
 * @returns {Promise<void>} A promise that resolves when the re-invocation request is complete.
 */
async function invokeNew(
  url,
  taskId,
  retryCount,
  totalTimeOfExecution,
  timeOfExecution
) {
  try {
    await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        taskId: taskId,
        retryCount: retryCount + 1,
        totalTimeOfExecution: totalTimeOfExecution + timeOfExecution,
      }),
    });
    // .then((response) => response.json())
    // .then((json) => console.log(json));
  } catch (error) {
    console.error(`Error re-invoking function for task ${taskId}:`, error);
  }
}
