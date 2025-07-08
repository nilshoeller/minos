# Minos – Thesis Implementation

This repository contains the implementation of my Bachelor's thesis on optimizing Function as a Service (FaaS) performance.

Below is an overview of the project structure and the most important directories to help you navigate the codebase.

> ⚠️ **Note**: This project has been taken down and is no longer executable.  
> It is published for reference purposes only — primarily to provide access to the collected data and logs.

---

## 📁 Directory Structure

### `gcpfunctions/`

Contains the Google Cloud Functions used in the project:

- **`function-baseline.go`**  
  The baseline function used for performance comparison.

- **`function-optimized.go`**  
  The optimized function that implements the performance improvement strategy.

- **`function-execute-benchmark.go`**  
  A helper function that measures how long benchmarks typically take.

---

### `jupyter/`

Jupyter notebooks and logs for experimentation and analysis:

- **`logs_analysis/`**  
  Contains daily log files collected during the experiment.

- **`workflow-1/`**  
  Notebooks for executing the experiment workflow.

- **`workflow-2/`**  
  Notebooks for analyzing the experimental results.

---

### `loadtesting/`

Contains scripts for running load tests using [k6](https://k6.io/).

---

## 📝 Notes

We executed the experiment twice to ensure a backup in case of issues. Since the first run completed without problems, only the data from the first execution was used in our analysis.
