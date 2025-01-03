import { useRef, useEffect, useState } from 'react'

import _ from 'lodash';

import { io } from 'socket.io-client';
import './App.css'
import View  from './Visualization';


function App() {

  const [assembly, setAssembly] = useState({})
  const [tracks, setTracks] = useState([])
  const [jbrowse, showJbrowse] = useState(false)
  const socketUrl = "ws://127.0.0.1:8000/ws";


  useEffect(() => {

    const socket = new WebSocket(socketUrl);

    socket.onopen = () => {
      console.log("WebSocket connection established.");
    };
    
    socket.onopen = () => {
      console.log("WebSocket connection established.");
  };

    socket.onmessage = (event) => {
      const incoming_data = JSON.parse(event.data);
      console.log(incoming_data)
      if (incoming_data && !_.isEqual(incoming_data.assembly, assembly) && !_.isEqual(incoming_data.track, tracks)) {
        console.log(incoming_data.assembly)
        setAssembly(incoming_data.assembly)
        setTracks(incoming_data.track)
        showJbrowse(true)
      }
  };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
      console.log("websocket connection closed")
    }
  // Cleanup on component unmount
  return () => {
    // socket.close();

  };
}, [jbrowse]);


  return (
    <>
    <div>Hello</div>

    {/* {jbrowse && < View assembly={assembly} tracks={tracks} /> } */}
   
    </>
  )
}

export default App