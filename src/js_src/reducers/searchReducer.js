const FIXTURE_STATE = {
  query: 'ortholog',
  href: '',
  results: [
    {
      symbol: 'NTPCR',
      source: 'MGI',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000,
      organism: 'Mus musculus'
    },
    {
      symbol: 'Brca2',
      source: 'ZFIN',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000,
      organism: 'Danio rerio'
    },
    {
      symbol: 'Ctag2',
      source: 'MGI',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000,
      organism: 'Mus musculus'
    },
    {
      symbol: 'ntpcr',
      source: 'ZFIN',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000,
      organism: 'Danio rerio'
    },
    {
      symbol: 'rad54',
      source: 'SGD',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000,
      organism: 'Saccharomyces cerevisiae'
    }
  ]
};

const searchReducer = function () {
  return FIXTURE_STATE;
};

export default searchReducer;
