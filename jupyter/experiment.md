# EXPERIMENT SETUP

1. Make the experiment on weekdays, at the same time.
2. Re-deploy the cloud functions to start fresh, each function with an empty pool of instances.
3. Run the OPTIMIZED and the BASELINE function with 10 vus for 5 min, each vu making a request every 10 sec, totaling to 300 request per run
4. Calculate metrics
5. Generate graphics
