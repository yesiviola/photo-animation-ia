import axios from "axios";

const api = axios.create({
  baseURL: "/api",
    headers: {
        "Content-Type": "application/json",
    },
});

export function login(data) {
  return api.post(
    "/auth/login",
    data,
    { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
  );
}

export default api;
