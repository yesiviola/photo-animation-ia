import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import styles from "./RegisterPage.module.css";

function RegisterPage() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    full_name: "",
  });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const params = new URLSearchParams();
      params.append("username", formData.username);
      params.append("email", formData.email);
      params.append("password", formData.password);
      params.append("full_name", formData.full_name);
      
    
      const { data } = await axios.post("/auth/register", params);
      
      localStorage.setItem("access_token", data.access_token);
      navigate("/");
    } catch (error) {
      console.error("Register error:", error);
      setMessage(error.response?.data?.detail || "Error al registrarse");
    }
  };

  return (
    <div className={styles.registerContainer}>
      <h2 className={styles.title}>Registrarse</h2>
      <form onSubmit={handleSubmit} className={styles.form}>
        <label className={styles.label}>Usuario</label>
        <input
          name="username"
          value={formData.username}
          onChange={handleChange}
          className={styles.input}
          required
        />
        <label className={styles.label}>Correo</label>
        <input
          name="email"
          value={formData.email}
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
        <label className={styles.label}>Nombre completo</label>
        <input
          name="full_name"
          value={formData.full_name}
          onChange={handleChange}
          className={styles.input}
          required
        />
        <button type="submit" className={styles.button}>Registrarse</button>
      </form>
      {message && <p className={styles.message}>{message}</p>}
    </div>
  );
}

export default RegisterPage;