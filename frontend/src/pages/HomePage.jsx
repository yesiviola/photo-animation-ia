import React from "react";
import Carousel from "../components/Carousel";
import styles from "./HomePage.module.css";

function HomePage() {
  const images = [
    "/images/slide1.webp",
    "/images/slide2.webp",
    "/images/slide3.webp"
  ];

  return (
    <div className={styles.homeContainer}>
      <h1 className={styles.title}>Bienvenido a Photo Animation IA</h1>
      <p className={styles.subtitle}>
        Regístrate o inicia sesión para comenzar a subir y animar tus fotos.
      </p>
      <Carousel images={images} autoPlay={true} interval={3000} />
    </div>
  );
}

export default HomePage;
