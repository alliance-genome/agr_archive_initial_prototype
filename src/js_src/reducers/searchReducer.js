const FIXTURE_STATE = {
  query: 'ortholog',
  href: '',
  results: [
    {
      symbol: 'NTPCR',
      name: 'RADiation sensitive',
      geneId: 'MGI:12345678',
      sourceHref: 'https://www.google.com',
      synonyms: 'geneA, geneB',
      geneType: 'ORF',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000,
      species: 'Mus musculus',
      description: 'lore ipsum <mark>kinase</mark> sit onsectetur adipiscing elit, sed do eiusmod',
      highlights: {
        description: ['lorem ipsum <mark>kinase</mark> sit onsectetur adipiscing elit, sed do eiusmod']
      }
    },
    {
      symbol: 'Brca2',
      name: 'RADiation sensitive',
      geneId: 'ZFIN:12345678',
      sourceHref: 'https://www.google.com',
      synonyms: 'geneA, geneB',
      geneType: 'ORF',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000,
      species: 'Danio rerio',
      description: 'lorem ipsum <mark>kinase</mark> sit onsectetur adipiscing elit, sed do eiusmod',
      highlights: {
        description: ['lorem ipsum <mark>kinase</mark> sit onsectetur adipiscing elit, sed do eiusmod']
      }
    },
    {
      symbol: 'Ctag2',
      name: 'RADiation sensitive',
      geneId: 'MGI:12345678',
      sourceHref: 'https://www.google.com',
      synonyms: 'geneA, geneB',
      geneType: 'ORF',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000,
      species: 'Mus musculus',
      description: 'lorem ipsum <mark>kinase</mark> sit onsectetur adipiscing elit, sed do eiusmod',
      highlights: {
        description: ['lorem ipsum <mark>kinase</mark> sit onsectetur adipiscing elit, sed do eiusmod']
      }
    },
    {
      symbol: 'ntpcr',
      name: 'RADiation sensitive',
      geneId: 'ZFIN:12345678',
      sourceHref: 'https://www.google.com',
      synonyms: 'geneA, geneB',
      geneType: 'ORF',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000,
      species: 'Danio rerio',
      description: 'lorem ipsum <mark>kinase</mark> sit onsectetur adipiscing elit, sed do eiusmod',
      highlights: {
        description: ['lorem ipsum <mark>kinase</mark> sit onsectetur adipiscing elit, sed do eiusmod']
      }
    },
    {
      symbol: 'rad54',
      geneId: 'SGD:12345678',
      sourceHref: 'https://www.google.com',
      synonyms: 'geneA, geneB',
      geneType: 'ORF',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000,
      species: 'Saccharomyces cerevisiae',
      description: 'lorem ipsum <mark>kinase</mark> sit onsectetur adipiscing elit, sed do eiusmod',
      highlights: {
        description: ['lorem ipsum <mark>kinase</mark> sit onsectetur adipiscing elit, sed do eiusmod']
      }
    }
  ],
  total: 5,
  isPending: false
};

const searchReducer = function () {
  return FIXTURE_STATE;
};

export default searchReducer;
