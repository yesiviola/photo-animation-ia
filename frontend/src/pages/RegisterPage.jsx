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

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const { data } = await axios.post("/api/auth/register", formData);
      setMessage(data.message);
      navigate("/login");
    } catch (error) {
      console.error("Register error:", error);
      setMessage(error.response?.data?.detail || "Error al registrar");
    }
  };

  return (
    <div className={styles.registerContainer}>
      <h2 className={styles.title}>Registro de Usuario</h2>
      <form onSubmit={handleSubmit} className={styles.form}>
        <label className={styles.label}>Username</label>
        <input
          name="username"
          value={formData.username}
          onChange={handleChange}
          className={styles.input}
          required
        />

        <label className={styles.label}>Email</label>
        <input
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          className={styles.input}
          required
        />

        <label className={styles.label}>Password</label>
        <input
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          className={styles.input}
          required
        />

        <label className={styles.label}>Nombre Completo (opcional)</label>
        <input
          name="full_name"
          value={formData.full_name}
          onChange={handleChange}
          className={styles.input}
        />

        <button type="submit" className={styles.button}>
          Registrar
        </button>
      </form>
      {message && <p className={styles.message}>{message}</p>}
    </div>
  );
}

export default RegisterPage;