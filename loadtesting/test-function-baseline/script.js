import http from "k6/http";
import { sleep, check } from "k6";

const url =
  "https://europe-west3-bsc-thesis-implementation.cloudfunctions.net/baselineFunction";

export const options = {
  vus: 1,
  duration: "120s",
};

// Run with: k6 run script.js
export default function () {
  const response = http.get(url);

  // Check if the response status is OK (200)
  check(response, {
    "status 200": (r) => r.status === 200,
  });

  sleep(10);
}
