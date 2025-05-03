import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <h2>Photo Animation IA</h2>
      <ul>
        <li><Link to="/">Inicio</Link></li>
        <li><Link to="/register">Registro</Link></li>
        <li><Link to="/login">Login</Link></li>
        <li><Link to="/upload">Subir Imagen</Link></li>
        <li><Link to="/animate">Animar Imagen</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;
