import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomePage from "./pages/HomePage";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import UploadPage from "./pages/UploadPage";
import AnimatePage from "./pages/AnimatePage";
import Footer from "./components/Footer";  // Importa el Footer

function App() {
  return (
    <div style={{display: "flex", flexDirection: "column", minHeight: "100vh"}}>
      <Navbar />
      <div style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/animate" element={<AnimatePage />} />
        </Routes>
      </div>
      <Footer />
    </div>
  );
}

export default App;
