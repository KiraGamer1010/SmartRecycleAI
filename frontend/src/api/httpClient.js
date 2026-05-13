import axios from "axios";
import { appConfig } from "../config/env.js";

export const httpClient = axios.create({
  baseURL: appConfig.apiBaseUrl,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json"
  }
});
