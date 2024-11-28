import http from "k6/http";
import { sleep, check } from "k6";

const url =
  __ENV.URL ||
  "https://europe-west3-bsc-thesis-implementation.cloudfunctions.net/optimizedFunction";

export const options = {
  vus: __ENV.VUS ? parseInt(__ENV.VUS) : 1,
  duration: __ENV.DURATION || "120s",
};

// Run with: k6 run --env URL=<"your-url"> --env VUS=5 --env DURATION=<"60s"> script.js
export default function () {
  const response = http.get(url);

  // Check if the response status is OK (200)
  check(response, {
    "status 200": (r) => r.status === 200,
  });

  sleep(5);
}
