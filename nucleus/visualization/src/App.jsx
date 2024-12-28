import { useRef, useEffect, useState } from 'react'

import _ from 'lodash';

import { io } from 'socket.io-client';
import './App.css'
import View  from './Visualization';


function App() {

  const [assembly, setAssembly] = useState({})
  const [tracks, setTracks] = useState([])
  const [jbrowse, showJbrowse] = useState(false)


  useEffect(() => {
    const socket = io('http://127.0.0.1:5000');

    try {
    socket.on('data', (incoming_data) => {

      if (incoming_data?.config && !_.isEqual(incoming_data.config.assembly, assembly) && !_.isEqual(incoming_data.config.track, tracks)) {

        console.log(incoming_data.config.assembly)
        setAssembly(incoming_data.config.assembly)
        setTracks(incoming_data.config.track)
        showJbrowse(true)

      }
    });

  } catch (err) {
    console.error("Failed to parse event data:", err);
  }
 
    return () => {
      console.log("Cleaning up WebSocket listeners");
      socket.off('data');
      // socket.disconnect();
    };
  }, [jbrowse]);

  return (
    <>
    <div>Hello</div>
    {jbrowse && < View assembly={assembly} tracks={tracks} /> }
   
    </>
  )
}

export default App
