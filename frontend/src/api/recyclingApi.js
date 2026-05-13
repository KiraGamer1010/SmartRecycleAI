import { httpClient } from "./httpClient.js";

export async function getSystemHealth() {
  const { data } = await httpClient.get("/health");
  return data;
}

export async function getWasteScans() {
  const { data } = await httpClient.get("/api/v1/recycling/scans");
  return data;
}

export async function createWasteScan(payload) {
  const { data } = await httpClient.post("/api/v1/recycling/scans", payload);
  return data;
}
