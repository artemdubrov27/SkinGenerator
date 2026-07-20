import React from "react";
import { useLoader } from "@react-three/fiber";
import { TextureLoader } from "three";

function MinecraftCharacter({ url }) {
  const texture = useLoader(TextureLoader, url);

  return (
    <group>
      {/* Голова */}
      <mesh position={[0, 1.5, 0]}>
        <boxGeometry args={[0.8, 0.8, 0.8]} />
        <meshStandardMaterial map={texture} />
      </mesh>

      {/* Тіло */}
      <mesh position={[0, 0.6, 0]}>
        <boxGeometry args={[0.9, 1.2, 0.4]} />
        <meshStandardMaterial map={texture} />
      </mesh>

      {/* Руки */}
      <mesh position={[-0.7, 0.6, 0]}>
        <boxGeometry args={[0.3, 1.2, 0.4]} />
        <meshStandardMaterial map={texture} />
      </mesh>
      <mesh position={[0.7, 0.6, 0]}>
        <boxGeometry args={[0.3, 1.2, 0.4]} />
        <meshStandardMaterial map={texture} />
      </mesh>

      {/* Ноги */}
      <mesh position={[-0.25, -0.6, 0]}>
        <boxGeometry args={[0.4, 1.2, 0.4]} />
        <meshStandardMaterial map={texture} />
      </mesh>
      <mesh position={[0.25, -0.6, 0]}>
        <boxGeometry args={[0.4, 1.2, 0.4]} />
        <meshStandardMaterial map={texture} />
      </mesh>
    </group>
  );
}

export default MinecraftCharacter;
