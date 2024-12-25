import React, { useState } from 'react';
import Terminal from './components/Terminal';

function App() {
  const [terminalHeight, setTerminalHeight] = useState(20); // Initial height as percentage

  const increaseHeight = () => {
    setTerminalHeight((prev) => Math.min(prev + 5, 100)); // Max height at 100%
  };

  const decreaseHeight = () => {
    setTerminalHeight((prev) => Math.max(prev - 5, 0)); // Min height at 0%
  };

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <h1 style={{ textAlign: 'center' }}>Web Terminal</h1>
      <div style={{ flex: 1, backgroundColor: '#f0f0f0' }} />
      <div
        style={{
          height: `${terminalHeight}%`,
          backgroundColor: '#333',
          color: '#fff',
          padding: '10px',
          overflow: 'auto',
        }}
      >
        <Terminal />
      </div>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#444',
          color: '#fff',
          cursor: 'pointer',
          height: '30px',
        }}
      >
        <button
          onClick={increaseHeight}
          style={{
            background: 'none',
            border: 'none',
            color: 'inherit',
            fontSize: '16px',
            cursor: 'pointer',
            padding: '5px',
          }}
        >
          ▲
        </button>
        <button
          onClick={decreaseHeight}
          style={{
            background: 'none',
            border: 'none',
            color: 'inherit',
            fontSize: '16px',
            cursor: 'pointer',
            padding: '5px',
          }}
        >
          ▼
        </button>
      </div>
    </div>
  );
}

export default App;
