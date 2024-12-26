const addTrack = (trackIDsRef, setTracks, setShowTrack, viewState, all_tracks) => {
  
  const trackId = 'genes'
    const new_track_addition =  {
        type: 'AlignmentsTrack',
        trackId: trackId, 
        name: 'spike-in_bams_file_0.bam',
        assemblyNames: ['NC_045512'],
        category: ['Genes'],
        adapter: {
          type: 'BamAdapter',
          bamLocation: {
            uri: 'http://127.0.0.1:5000/uploads/data/bamfiles/customised_my_vcf_NODE-1.bam',
          },
          index: {
            location: {
              uri: 'http://127.0.0.1:5000/uploads/data/bamfiles/customised_my_vcf_NODE-1.bam.bai',
            },
          },
        }
    }

    if (!trackIDsRef.current.includes(trackId))
      {
        console.log("inside")
          setTracks([...all_tracks, new_track_addition])
          viewState.session.addTrackConf(new_track_addition);
      
          trackIDsRef.current = [...trackIDsRef.current, trackId];
          setShowTrack(trackId);
      }

    viewState.session.addTrackConf(new_track_addition);

}

export default addTrack