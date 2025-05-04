import React, { useState } from "react";
import axios from "axios";
import styles from "./AnimatePage.module.css";

export default function AnimatePage() {
  const [imageId, setImageId] = useState("");
  const [videoFile, setVideoFile] = useState(null);
  const [videoPreview, setVideoPreview] = useState("");
  const [drivingVideoId, setDrivingVideoId] = useState("");
  const [message, setMessage] = useState("");
  const token = localStorage.getItem("access_token");

  const handleImageIdChange = (e) => {
    setImageId(e.target.value);
    setMessage("");
  };

  const handleVideoFileChange = (e) => {
    const f = e.target.files[0];
    if (!f) return;
    setVideoFile(f);
    setVideoPreview(URL.createObjectURL(f));
    setDrivingVideoId("");
    setMessage("");
  };

  const handleVideoUpload = async () => {
    if (!videoFile) {
      setMessage("Selecciona un video primero");
      return;
    }
    const form = new FormData();
    form.append("file", videoFile);
    try {
      const { data } = await axios.post("/videos/upload", form, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`,
        },
      });
      setDrivingVideoId(data.video_id);
      setMessage("Video subido con éxito");
    } catch (err) {
      console.error("Error al subir video:", err);
      setMessage("Error al subir el video");
    }
  };

  const handleAnimate = async () => {
    if (!imageId.trim()) {
      setMessage("Por favor ingresa el ID de la imagen");
      return;
    }
    setMessage("Generando animación…");
    try {
    
      const { data } = await axios.post(
        "/animation/animate",
        null,
        {
          params: {
            image_id: imageId.trim(),
            driving_video_id: drivingVideoId.trim() || undefined,
          },
          headers: {
            Authorization: `Bearer ${token}`,
          },
          timeout: 300000,
        }
      );
      setMessage(`Animación lista: ${data.s3_url}`);
    } catch (err) {
      console.error("Animate error:", err);
      const detail = err.response?.data?.detail;
      setMessage(detail ? JSON.stringify(detail) : "Error al animar la imagen");
    }
  };

  return (
    <div className={styles.animateContainer}>
      <h2 className={styles.title}>Animar Imagen</h2>
      <div className={styles.field}>
        <label>ID de la Imagen</label>
        <input
          className={styles.input}
          value={imageId}
          onChange={handleImageIdChange}
          placeholder="Ingresa el ID de la imagen"
        />
      </div>
      <div className={styles.field}>
        <label>Subir video (opcional)</label>
        <input
          type="file"
          accept="video/*"
          className={styles.input}
          onChange={handleVideoFileChange}
        />
        <button className={styles.buttonSmall} onClick={handleVideoUpload}>
          Subir video
        </button>
      </div>
      {videoPreview && (
        <video className={styles.previewVideo} src={videoPreview} controls />
      )}
      {drivingVideoId && (
        <p className={styles.idText}>ID de video: {drivingVideoId}</p>
      )}
      <button className={styles.button} onClick={handleAnimate}>
        Animar
      </button>
      {message && <p className={styles.message}>{message}</p>}
    </div>
  );
}