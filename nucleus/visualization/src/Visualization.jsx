/* eslint-disable react/prop-types */
import { useState, useEffect } from 'react'
import { createRoot, hydrateRoot } from 'react-dom/client'

import '@fontsource/roboto'
import {
  createViewState,
  JBrowseLinearGenomeView,
} from '@jbrowse/react-linear-genome-view'

import defaultSession from './defaultSession'


function View({ assembly, tracks }) {
    const [viewState, setViewState] = useState()
    const [patches, setPatches] = useState('')
  
  
    useEffect(() => {
      const state = createViewState({
        assembly,
        tracks,
        defaultSession,
  
        onChange: patch => {
          setPatches(previous => previous + JSON.stringify(patch) + '\n')
        },
        configuration: {
          rpc: {
            defaultDriver: 'WebWorkerRpcDriver',
          },
        },
        makeWorkerInstance: () => {
          return new Worker(new URL('./rpcWorker', import.meta.url), {
            type: 'module',
          })
        },
  
        hydrateFn: hydrateRoot,
        createRootFn: createRoot,
      })
      setViewState(state)
    }, [assembly, tracks]) // Add dependencies to reinitialize on prop changes
  
    if (!viewState) {
      return null
    }
  
    return (
      <>
        <h1>JBrowse 2 React Linear Genome View Demo w/ Vite</h1>
        <JBrowseLinearGenomeView viewState={viewState} />
      </>
    )
  }
  
  export default View
  