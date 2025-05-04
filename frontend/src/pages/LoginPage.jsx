import React, { useState } from "react";
import axios from "../axiosConfig";
import { useNavigate } from "react-router-dom";
import styles from "./LoginPage.module.css";

function LoginPage() {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const params = new URLSearchParams();
      params.append("username", formData.username);
      params.append("password", formData.password);
      const { data } = await axios.post("/auth/login", params);
      localStorage.setItem("access_token", data.access_token);
      navigate("/");
    } catch (error) {
      console.error("Login error:", error);
      setMessage(error.response?.data?.detail || "Error al iniciar sesión");
    }
  };

  return (
    <div className={styles.loginContainer}>
      <h2 className={styles.title}>Iniciar Sesión</h2>
      <form onSubmit={handleSubmit} className={styles.form}>
        <label className={styles.label}>Usuario</label>
        <input
          name="username"
          value={formData.username}
          onChange={handleChange}
          className={styles.input}
          required
        />
        <label className={styles.label}>Contraseña</label>
        <input
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          className={styles.input}
          required
        />
        <button type="submit" className={styles.button}>Login</button>
      </form>
      {message && <p className={styles.message}>{message}</p>}
    </div>
  );
}

export default LoginPage;