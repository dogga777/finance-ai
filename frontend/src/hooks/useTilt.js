import { useRef, useState, useCallback } from "react";

/**
 * Returns props to attach to any element for a 3D tilt effect
 * that follows the mouse cursor.
 */
export function useTilt({ max = 8, scale = 1.02, speed = 220 } = {}) {
  const ref = useRef(null);
  const [style, setStyle] = useState({
    transform: "perspective(900px) rotateX(0deg) rotateY(0deg) scale(1)",
    transition: `transform ${speed}ms cubic-bezier(0.4, 0, 0.2, 1)`,
    transformStyle: "preserve-3d",
  });

  const onMouseMove = useCallback(
    (e) => {
      const el = ref.current;
      if (!el) return;
      const rect = el.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      const rotX = (-y * max).toFixed(2);
      const rotY = (x * max).toFixed(2);
      setStyle({
        transform: `perspective(900px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale(${scale})`,
        transition: `transform ${speed}ms cubic-bezier(0.4, 0, 0.2, 1)`,
        transformStyle: "preserve-3d",
      });
    },
    [max, scale, speed]
  );

  const onMouseLeave = useCallback(() => {
    setStyle({
      transform: "perspective(900px) rotateX(0deg) rotateY(0deg) scale(1)",
      transition: `transform ${speed}ms cubic-bezier(0.4, 0, 0.2, 1)`,
      transformStyle: "preserve-3d",
    });
  }, [speed]);

  return { ref, style, onMouseMove, onMouseLeave };
}
