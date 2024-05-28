import React, { useState, useRef } from 'react';

function AudioPlayer() {
  const [text, setText] = useState('');
  const [voice, setVoice] = useState('Joanna');
  const audioRef = useRef(null);

  const handleSynthesize = async () => {
    const response = await fetch('http://localhost:5000/synthesize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text, voice })
    });

    if (response.ok) {
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      audioRef.current.src = url;
      audioRef.current.play();
    } else {
      console.error('Failed to synthesize text');
    }
  };

  return (
    <div>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <select value={voice} onChange={(e) => setVoice(e.target.value)}>
        <option value="Joanna">Joanna (English - US)</option>
        <option value="Amy">Amy (English - UK)</option>
        <option value="Raveena">Raveena (Indian English)</option>
        // Add more options for other voices/languages here
      </select>
      <button onClick={handleSynthesize}>Convertir y Reproducir</button>
      <audio ref={audioRef} controls />
    </div>
  );
}

export default AudioPlayer;
