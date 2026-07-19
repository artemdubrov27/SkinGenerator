import React from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, useTexture } from "@react-three/drei";

function SkinModel({ texture }) {
  const tex = useTexture(texture);
  return (
    <mesh>
      <boxGeometry args={[1, 2, 0.5]} />
      <meshStandardMaterial map={tex} />
    </mesh>
  );
}

export default function SkinViewer({ texture }) {
  return (
    <Canvas style={{ background: "white", height: "80vh" }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[2, 2, 2]} />
      <SkinModel texture={texture} />
      <OrbitControls />
    </Canvas>
  );
}
