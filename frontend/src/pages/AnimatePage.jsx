import React, { useState } from "react";
import axios from "axios";

export default function AnimatePage() {
  const [imageId, setImageId] = useState("");
  const [drivingVideoId, setDrivingVideoId] = useState("");
  const [message, setMessage] = useState("");
  const token = localStorage.getItem("access_token");

  const handleAnimate = async () => {
    if (!imageId.trim()) {
      setMessage("Por favor ingresa el ID de la imagen");
      return;
    }
    
    try {
      const config = {
        params: {
          image_id: imageId.trim(),
          driving_video_id: drivingVideoId.trim() || undefined,
        },
        headers: {
          Authorization: `Bearer ${token}`,
        },
        timeout: 300000, // Timeout de 5 minutos
      };

      // Enviar la solicitud sin body (pasamos "undefined")
      const { data } = await axios.post("/api/animation/animate", undefined, config);
      
      console.log("Animate response:", data);
      setMessage(`Animación generada: ${data.s3_url}`);
    } catch (err) {
      console.error("Animate error:", err);
      const detail = err.response?.data?.detail;
      setMessage(detail ? JSON.stringify(detail) : "Error al animar la imagen");
    }
  };

  return (
    <div className="animate-container">
      <h2>Animar Imagen</h2>
      <label>ID de la Imagen</label>
      <input
        value={imageId}
        onChange={(e) => setImageId(e.target.value)}
        placeholder="Ingresa el ID de la imagen"
      />
      <label>ID de Video (opcional)</label>
      <input
        value={drivingVideoId}
        onChange={(e) => setDrivingVideoId(e.target.value)}
        placeholder="Ingresa el ID del video (opcional)"
      />
      <button onClick={handleAnimate}>Animar</button>
      {message && <p style={{ marginTop: 12 }}>{message}</p>}
    </div>
  );
}