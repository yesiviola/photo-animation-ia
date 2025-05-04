import axios from "axios";

// Usamos la ruta relativa para que el proxy de Vite redirija
axios.defaults.baseURL = "/api";

// Agregamos un interceptor para ver la URL final en consola
axios.interceptors.request.use((config) => {
  console.log("Request URL:", config.baseURL + config.url);
  return config;
});

export default axios;