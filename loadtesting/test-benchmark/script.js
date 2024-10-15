import http from "k6/http";
import { sleep, check } from "k6";
import { Trend, Counter } from "k6/metrics";

const url =
  "https://europe-west3-bsc-thesis-implementation.cloudfunctions.net/executeBenchmark";

const totalDurationTrend = new Trend("total_duration");
const reqCounter = new Counter("reqCounter");

export const options = {
  vus: 2,
  duration: "30s",
  thresholds: {
    total_duration: ["avg < 0.06", "p(95) < 0.08"],
    reqCounter: ["count>=0"],
  },
};

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

  sleep(5);
}

// export function handleSummary(data) {
//   console.log("HANDLE SUMMARY");

//   return {
//     "summary.json": JSON.stringify(data),
//   };
// }
