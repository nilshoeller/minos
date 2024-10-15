import http from "k6/http";
import { sleep } from "k6";

const url =
  "https://europe-west3-bsc-thesis-implementation.cloudfunctions.net/executeBenchmark";

export const options = {
  vus: 1,
  duration: "10s",
};

export default function () {
  http.get(url);
  sleep(1);
}
