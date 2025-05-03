import React, { useState, useEffect } from "react";
import styles from "./Carousel.module.css";

const Carousel = ({ images, autoPlay = true, interval = 3000 }) => {
  const [current, setCurrent] = useState(0);
  const length = images.length;

  useEffect(() => {
    let timer;
    if (autoPlay && length > 0) {
      timer = setInterval(() => {
        setCurrent((prev) => (prev + 1) % length);
      }, interval);
    }
    return () => clearInterval(timer);
  }, [autoPlay, interval, length]);

  if (!Array.isArray(images) || images.length === 0) return null;

  const nextSlide = () => {
    setCurrent((prev) => (prev + 1) % length);
  };

  const prevSlide = () => {
    setCurrent((prev) => (prev - 1 + length) % length);
  };

  return (
    <div className={styles.carousel}>
      <button onClick={prevSlide} className={styles.leftArrow}>
        &#10094;
      </button>
      <button onClick={nextSlide} className={styles.rightArrow}>
        &#10095;
      </button>
      {images.map((img, index) => (
        <div
          key={index}
          className={`${styles.slide} ${index === current ? styles.active : ""}`}
        >
          {index === current && (
            <img src={img} alt={`slide ${index}`} className={styles.image} />
          )}
        </div>
      ))}
    </div>
  );
};

export default Carousel;
