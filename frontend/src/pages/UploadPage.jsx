import React, { useState } from "react";
import axios from "axios";
import styles from "./UploadPage.module.css";

function UploadPage() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [uploadId, setUploadId] = useState("");
  const [message, setMessage] = useState("");
  const [copied, setCopied] = useState(false);
  const token = localStorage.getItem("access_token");

  const handleFileChange = (e) => {
    const f = e.target.files[0];
    if (!f) return;
    setFile(f);
    setPreviewUrl(URL.createObjectURL(f));
    setUploadId("");
    setMessage("");
    setCopied(false);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Selecciona un archivo primero");
      return;
    }
    const form = new FormData();
    form.append("file", file);

    try {
      const { data } = await axios.post("/images/upload", form, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setUploadId(data.image_id);
      setMessage("¡Imagen subida con éxito!");
      setCopied(false);
    } catch (err) {
      console.error("Upload error:", err);
      setMessage("Error al subir la imagen");
    }
  };

  const handleCopy = () => {
    if (!uploadId) return;
    navigator.clipboard.writeText(uploadId).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className={styles.uploadContainer}>
      <input
        type="file"
        onChange={handleFileChange}
        className={styles.inputFile}
        accept="image/*"
      />

      <button onClick={handleUpload} className={styles.button}>
        Subir Imagen
      </button>

      {previewUrl && (
        <img
          src={previewUrl}
          alt="Vista previa"
          className={styles.preview}
        />
      )}

      {message && <p className={styles.message}>{message}</p>}

      {uploadId && (
        <div className={styles.idRow}>
          <span className={styles.idText}>{uploadId}</span>
          <button
            onClick={handleCopy}
            className={styles.copyButton}
          >
            {copied ? "¡Copiado!" : "Copiar"}
          </button>
        </div>
      )}
    </div>
  );
}

export default UploadPage;
