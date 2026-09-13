import { useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Float, OrbitControls } from "@react-three/drei";

function CoreOrb() {
  const outer = useRef();
  const inner = useRef();
  const ringA = useRef();
  const ringB = useRef();

  useFrame((state) => {
    const t = state.clock.elapsedTime;
    if (outer.current) {
      outer.current.rotation.y = t * 0.35;
      outer.current.rotation.x = t * 0.18;
    }
    if (inner.current) {
      inner.current.rotation.y = -t * 0.6;
    }
    if (ringA.current) {
      ringA.current.rotation.z = t * 0.5;
      ringA.current.rotation.x = Math.PI / 3 + Math.sin(t * 0.3) * 0.15;
    }
    if (ringB.current) {
      ringB.current.rotation.z = -t * 0.4;
      ringB.current.rotation.x = Math.PI / 2 + Math.cos(t * 0.35) * 0.2;
    }
  });

  return (
    <group>
      {/* Outer wireframe icosahedron */}
      <mesh ref={outer}>
        <icosahedronGeometry args={[1.35, 1]} />
        <meshBasicMaterial color="#8b5cf6" wireframe transparent opacity={0.55} />
      </mesh>

      {/* Inner glowing sphere */}
      <mesh ref={inner}>
        <icosahedronGeometry args={[0.65, 0]} />
        <meshStandardMaterial
          color="#6366f1"
          emissive="#6366f1"
          emissiveIntensity={1.4}
          roughness={0.2}
          metalness={0.6}
        />
      </mesh>

      {/* Orbiting ring A */}
      <mesh ref={ringA}>
        <torusGeometry args={[1.85, 0.008, 16, 128]} />
        <meshBasicMaterial color="#a5b4fc" transparent opacity={0.7} />
      </mesh>

      {/* Orbiting ring B */}
      <mesh ref={ringB}>
        <torusGeometry args={[2.05, 0.006, 16, 128]} />
        <meshBasicMaterial color="#ec4899" transparent opacity={0.55} />
      </mesh>

      {/* Ambient glow balls */}
      <ambientLight intensity={0.7} />
      <pointLight position={[3, 3, 3]} intensity={1.4} color="#6366f1" />
      <pointLight position={[-3, -3, -3]} intensity={1.0} color="#8b5cf6" />
      <pointLight position={[0, 0, 4]} intensity={0.6} color="#ec4899" />
    </group>
  );
}

function Particles() {
  const group = useRef();

  const positions = [];
  for (let i = 0; i < 180; i++) {
    const r = 2.4 + Math.random() * 1.6;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    positions.push(
      r * Math.sin(phi) * Math.cos(theta),
      r * Math.sin(phi) * Math.sin(theta),
      r * Math.cos(phi)
    );
  }

  useFrame((state) => {
    if (group.current) {
      group.current.rotation.y = state.clock.elapsedTime * 0.08;
      group.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.15) * 0.15;
    }
  });

  return (
    <group ref={group}>
      <points>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={positions.length / 3}
            array={new Float32Array(positions)}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          color="#c7d2fe"
          size={0.03}
          sizeAttenuation
          transparent
          opacity={0.75}
        />
      </points>
    </group>
  );
}

export default function Hero3D() {
  return (
    <div className="hero-3d-canvas">
      <Canvas
        camera={{ position: [0, 0, 5.5], fov: 45 }}
        dpr={[1, 1.8]}
        gl={{ antialias: true, alpha: true }}
      >
        <Float speed={1.3} rotationIntensity={0.4} floatIntensity={0.6}>
          <CoreOrb />
        </Float>
        <Particles />
        <OrbitControls
          enableZoom={false}
          enablePan={false}
          rotateSpeed={0.4}
          autoRotate={false}
        />
      </Canvas>
    </div>
  );
}
