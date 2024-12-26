import {useState, useRef, useEffect} from 'react'
import { createRoot, hydrateRoot } from 'react-dom/client'
import { io } from 'socket.io-client';
import './App.css';
// import assembly from './assembly';
import defaultSession from './defaultSession'
import makeWorkerInstance from '@jbrowse/react-linear-genome-view/esm/makeWorkerInstance'

import {
  createViewState,
  JBrowseLinearGenomeView,
} from '@jbrowse/react-linear-genome-view'

import assembly from './assembly';
import tracks from './tracks';
import addTrack from './components/tracks';

function App() {

    const socket = io('http://127.0.0.1:5000');
    const jbrowse_data = useRef(null)

     const [viewState, setViewState] = useState()
      const [patches, setPatches] = useState('')
      
      const [showTrack, setShowTrack] = useState(null)

      const [all_tracks, setTracks] = useState([])
      const [createTract, setCreateTrack] = useState(null)
      const trackIDsRef = useRef([]);

      const assemblyRef = useRef({})
      const trackRef = useRef([])

  // useEffect(() => {
  //   if(createTract){
  //       addTrack( 
  //         trackIDsRef, 
  //         setTracks, 
  //         setShowTrack, 
  //         viewState, 
  //         all_tracks);
  //       }
  //     setCreateTrack(false);
  //   }, [createTract])

    useEffect(() => {
      if(showTrack)
      {

        console.log("here ")
          trackIDsRef.current.forEach((trackId) => {
          viewState.session.view.showTrack(trackId);
          })

          viewState.session.view.showAllRegionsInAssembly(assemblyRef.current.name)
          setShowTrack(null)
          // setCreateTrack(false);
      }
      }, [showTrack])


  useEffect(() => {
    
    // Listen for messages from the server
    socket.on('data', (incoming_data) => {

      console.log("inc", incoming_data.message)
      if(!jbrowse_data.current && incoming_data.message !== jbrowse_data.current){
        jbrowse_data.current = incoming_data.message
        assemblyRef.current = jbrowse_data.current.assembly
        trackRef.current = jbrowse_data.current.track

        const state = createViewState({

          assembly: jbrowse_data.current.assembly,
          tracks:jbrowse_data.current.track,
          onChange: (patch) => {
            setPatches(previous => previous + JSON.stringify(patch) + '\n')
          },
          defaultSession,
          configuration: {
            rpc: {
              defaultDriver: 'WebWorkerRpcDriver',
            },
          },
          makeWorkerInstance,
    
          hydrateFn: hydrateRoot,
          createRootFn: createRoot,
    })

    // trackIDsRef.current = [...trackIDsRef.current, jbrowse_data.current.track[0].trackId];
        // console.log("trackid", trackRef.current[0].trackId)
        state.session.view.showTrack(trackRef.current[0].trackId)

        state.session.view.showAllRegionsInAssembly(assemblyRef.current.name)
        setViewState(state)
        // setShowTrack(true)
      }
    }); 
    // Cleanup connection on unmount
    return () => {
      socket.off('data');
    };
  }, []);

  // useEffect(() => {
  //   if (viewState){
  //     let assembly_name = assembly.name
  //     console.log("assembly_name", assembly_name)
  //     viewState.session.view.showAllRegionsInAssembly(assembly_name)
  //   }
  // }, [viewState])

  const click_me = () => {

    setCreateTrack(true)
    viewState.session.view.showAllRegionsInAssembly("NC_045512")
    
    // setData(true)
    
  }

    if (!viewState) {
      return null
    }
  return (
    <div className="App">
      <button onClick={click_me}> Click </button>
     <JBrowseLinearGenomeView viewState={viewState} />
    </div>
  );
}

export default App;
