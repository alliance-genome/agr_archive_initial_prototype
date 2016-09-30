const FIXTURE_STATE = {
  query: 'ortholog',
  href: '',
  results: [
    {
      symbol: 'rad54',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000
    },
    {
      symbol: 'dog1',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000
    },
    {
      symbol: 'ke4',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000
    },
    {
      symbol: 'ke4',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000
    },
    {
      symbol: 'ke4',
      genomicStartCoordinates: 100,
      genomicStopCoordinates: 1000,
      relativeStartCoordinates: 100,
      relativeStopCoordinates: 1000
    }
  ]
};

const searchReducer = function () {
  return FIXTURE_STATE;
};

export default searchReducer;
