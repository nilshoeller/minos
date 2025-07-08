# Load test GCP-Functions

To start both scripts and to load test the BASELINE and OPTIMIZED functions at the same time run:

`(cd ./test-function-baseline && k6 run script.js) & (cd ./test-function-optimized && k6 run script.js)`
