import { useState, useEffect } from 'react';

export function useIntro() {
  const [despertando, setDespertando] = useState(true);
  const [esconderIntro, setEsconderIntro] = useState(false);

  useEffect(() => {
    const timerIntro = setTimeout(() => {
      setDespertando(false);
      setTimeout(() => setEsconderIntro(true), 1500);
    }, 2500);
    return () => clearTimeout(timerIntro);
  }, []);

  return { despertando, esconderIntro };
}
