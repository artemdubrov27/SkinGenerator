import React, { useState } from "react";
import SkinViewer from "./components/SkinViewer";

function App() {
  const [photos, setPhotos] = useState([]);
  const [skinURL, setSkinURL] = useState(null);

  const handleFiles = (e) => setPhotos([...e.target.files]);

  const generateSkin = async () => {
    const formData = new FormData();
    photos.forEach((file, i) => formData.append(`file${i + 1}`, file));
    const response = await fetch("https://skingenerator.onrender.com/generate_skin", {
      method: "POST",
      body: formData
    });
    const blob = await response.blob();
    setSkinURL(URL.createObjectURL(blob));
  };

  return (
    <div style={{ backgroundColor: "#0b1a3a", height: "100vh", color: "white", padding: "20px" }}>
      <h2>Генератор скіна Minecraft</h2>
      <input type="file" multiple accept="image/*" onChange={handleFiles} />
      <button onClick={generateSkin}>Згенерувати скін</button>
      {skinURL && <SkinViewer texture={skinURL} />}
    </div>
  );
}

export default App;
