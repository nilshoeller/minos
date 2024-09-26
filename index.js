// deploy like this:
// gcloud functions deploy firstTestFunction --no-gen2 --entry-point testFunction --runtime nodejs20 --trigger-http --project bsc-thesis-implementation
exports.testFunction = (req, res) => {
  let message =
    req.query.message ||
    "You didn't specify any message in the message-query parameter";
  res.status(200).send(message);
};
