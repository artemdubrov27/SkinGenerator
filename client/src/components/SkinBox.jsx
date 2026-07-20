import React from "react";
import { useLoader } from "@react-three/fiber";
import { TextureLoader } from "three";

function SkinBox({ url }) {
  const texture = useLoader(TextureLoader, url);

  return (
    <mesh>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial map={texture} />
    </mesh>
  );
}

export default SkinBox;
