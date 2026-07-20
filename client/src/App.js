import React, { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { useLoader } from "@react-three/fiber";
import { TextureLoader } from "three";

// Старий куб (залишаємо для тесту сцени)
function Box() {
  return (
    <mesh>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="orange" />
    </mesh>
  );
}

// Новий куб із текстурою скіна
function SkinBox({ url }) {
  const texture = useLoader(TextureLoader, url);
  return (
    <mesh>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial map={texture} />
    </mesh>
  );
}

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

      {skinUrl && (
        <div>
          <h2>Generated Skin:</h2>
          <img src={skinUrl} alt="Generated Skin" style={{ maxWidth: "300px" }} />
        </div>
      )}

      <Canvas style={{ height: "400px", marginTop: "20px" }}>
        <ambientLight />
        <pointLight position={[10, 10, 10]} />
        {/* Якщо є скін — показуємо його, інакше старий куб */}
        {skinUrl ? <SkinBox url={skinUrl} /> : <Box />}
        <OrbitControls />
      </Canvas>
    </div>
  );
}

export default App;
