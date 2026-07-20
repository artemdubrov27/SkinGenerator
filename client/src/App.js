import React, { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import MinecraftCharacter from "./components/MinecraftCharacter";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [skinUrl, setSkinUrl] = useState(null);

  const handleFileUpload = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleGenerate = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const res = await fetch("http://127.0.0.1:8000/generate_skin", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setSkinUrl(data.skin_url);
    } catch (error) {
      console.error("Error generating skin:", error);
    }
  };

  return (
    <div>
      <h1>Skin Generator</h1>
      <input type="file" onChange={handleFileUpload} />
      <button onClick={handleGenerate}>Generate Skin</button>

      <Canvas style={{ height: "500px", marginTop: "20px" }}>
        <ambientLight />
        <pointLight position={[10, 10, 10]} />
        {skinUrl ? <MinecraftCharacter url={skinUrl} /> : null}
        <OrbitControls />
      </Canvas>
    </div>
  );
}

export default App;
