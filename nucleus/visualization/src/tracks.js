const tracks = [ 
    {
      type: 'AlignmentsTrack',
      trackId: 'genes',
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
  ]
  
  export default tracks