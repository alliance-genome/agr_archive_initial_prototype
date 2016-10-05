import _ from 'underscore';

const DEFAULT_STATE = {
  activeCategory: 'none',
  aggregations: [],
  errorMessage: '',
  isError: false,
  isPending: false,
  results: [],
  total: 0,
};

const searchReducer = function (_state, action) {
  let state = _.clone(_state);
  if (typeof state === 'undefined') {
    return DEFAULT_STATE;
  }
  switch(action.type) {
  case 'SEARCH_ERROR':
    state.errorMessage = action.payload;
    state.isError = true;
    return state;
  case 'SEARCH_RESPONSE':
    state.aggregations = [];
    state.isPending = false;
    state.total = action.payload.total;
    state.results = action.payload.results.map( d => {
      return {
        symbol: d.symbol,
        name: d.name,
        geneId: 'ID:12345678',
        sourceHref: 'https://www.google.com',
        synonyms: d.synonym,
        geneType: 'TYPE',
        genomicStartCoordinates: '',
        genomicStopCoordinates: '',
        relativeStartCoordinates: '',
        relativeStopCoordinates: '',
        species: d.organism,
        highlight: {
          disease: ['lorem ipsum <mark>huntington\'s</mark> sit onsectetur adipiscing elit, sed do eiusmod']
        }
      };
    });
    return state;
  default:
    return state;
  }
};

export default searchReducer;
