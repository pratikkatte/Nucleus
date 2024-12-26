const assembly = {
  name: 'NC_045512',
  aliases: ['hg38'],
  sequence: {
    type: 'ReferenceSequenceTrack',
    trackId: 'GRCh38-ReferenceSequenceTrack',
    adapter: {
      type: 'IndexedFastaAdapter',
      fastaLocation: {
        uri: 'http://127.0.0.1:5000/uploads/data/reference/NC_045512v2.fa',
      },
      faiLocation: {
        uri: 'http://127.0.0.1:5000/uploads/data/reference/NC_045512v2.fa.fai',
      },
    },
  }
}

export default assembly
