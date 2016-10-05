import _ from 'underscore';

import { injectHighlightIntoResponse } from '../lib/searchHelpers';

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
  // simple way to not alter original state
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
    state.results = action.payload.results.map( _d => {
      let d = injectHighlightIntoResponse(_d);
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
        highlight: d.highlights
      };
    });
    return state;
  default:
    return state;
  }
};

export default searchReducer;
