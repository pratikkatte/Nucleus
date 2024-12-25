import{ useEffect, useRef } from 'react';
import { Terminal } from '@xterm/xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';
import axios from 'axios';

const TerminalComponent = () => {
  const terminalRef = useRef(null);
  const inputBufferRef = useRef("");

  const fitAddon = new FitAddon();
  // const [inputBuffer, setInputBuffer] = useState(""); // Buffer for user input
  const BACKEND_URL = 'http://127.0.0.1:5000'; // Flask backend URL


  useEffect(() => {
    const terminal = new Terminal({
      theme: {
        background: '#1E1E1E', // Dark background
        foreground: '#C7C7C7', // Light gray text
        cursor: 'white', // Cursor color
        selection: 'rgba(255, 255, 255, 0.3)', // Selection highlight
      },
      fontSize: 14,
      fontFamily: 'Courier, monospace',
    });

    if (terminalRef.current) {
      terminal.open(terminalRef.current);
      fitAddon.fit();
    }


    // // Initial terminal message
    terminal.writeln('\x1b[32mWelcome to the Web Terminal\x1b[0m'); // Green text
    terminal.prompt = () => {
      terminal.write('\r\n\x1b[34m$ \x1b[0m'); // Blue dollar sign
    };
    terminal.prompt();

    // Handle terminal input

    terminal.onData((data) => {
      console.log(inputBufferRef)
      if (data === '\r') {
        const command = inputBufferRef.current.trim();
        if (command) {
          terminal.writeln('\n')
          executeCommand(command, terminal);
        }
        inputBufferRef.current = "";

      } else if (data === '\u007F') {
        if (inputBufferRef.current.length > 0) {
          inputBufferRef.current = inputBufferRef.current.slice(0, -1);
          terminal.write('\b \b');
        }
      } else {
        inputBufferRef.current += data;
        terminal.write(data);
      }
    });
  
    return () => {
      terminal.dispose();
    };
  }, []);

  // Function to send command to the backend and display output
  const executeCommand = async (command, terminal) => {
    try {
      const response = await axios.post(`${BACKEND_URL}/execute`, { command });
      if (response.data.output) {
        // terminal.write(`${data}`); // White for output
        const lines = response.data.output.split('\n');
        lines.forEach((line) => terminal.writeln(line));
      }
      if (response.data.error) {
        terminal.writeln(`\x1b[31mError: ${response.data.error}\x1b[0m`); // Red for errors
      }
    } catch (err) {
      console.log("error", err)
      terminal.writeln(`\x1b[31mFailed to connect to backend: ${err.message}\x1b[0m`); // Red for connection issues
      
    }
    terminal.prompt();
  };

  return (
  <div ref={terminalRef} style={{ flexGrow: 1, overflow: 'hidden' }} />
);
};

export default TerminalComponent;
