import React from "react";
import styles from "./Footer.module.css";

const Footer = () => {
  return (
    <footer className={styles.footer}>
      <p className={styles.text}>
        © {new Date().getFullYear()} Photo Animation IA. Creado por Yesenia González. Todos los derechos reservados.
      </p>
    </footer>
  );
};

export default Footer;
