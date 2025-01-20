import http from "k6/http";
import { sleep, check } from "k6";
import { Trend, Counter } from "k6/metrics";

const url =
  "https://europe-west3-bsc-thesis-implementation.cloudfunctions.net/executeBenchmark";

const totalDurationTrend = new Trend("total_duration");
const reqCounter = new Counter("reqCounter");

export const options = {
  vus: __ENV.VUS ? parseInt(__ENV.VUS) : 1,
  duration: __ENV.DURATION || "60s",
  summaryTrendStats: [
    "avg",
    "min",
    "med",
    "max",
    "p(60)",
    "p(65)",
    "p(90)",
    "p(95)",
  ],
  thresholds: {
    total_duration: ["avg < 0.06", "p(95) < 0.08"],
    reqCounter: ["count>=0"],
  },
};

// Run with: k6 run script.js
export default function () {
  const response = http.get(url);

  // Check if the response status is OK (200)
  check(response, {
    "status 200": (r) => r.status === 200,
  });

  // Parse the response body to extract the duration
  const responseBody = JSON.parse(response.body);
  const duration = responseBody.duration;

  // Accumulate the duration and increase the request count
  if (duration !== undefined) {
    totalDurationTrend.add(duration);
    reqCounter.add(1);
  }

  sleep(1);
}

export function handleSummary(data) {
  console.log("HANDLE SUMMARY");

  const summary = {
    reqCounter: data.metrics.reqCounter,
    total_duration: data.metrics.total_duration,
  };

  return {
    "summary.json": JSON.stringify(summary),
  };
}
