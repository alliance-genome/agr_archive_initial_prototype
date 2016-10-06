import _ from 'underscore';

import { injectHighlightIntoResponse } from '../lib/searchHelpers';

const MAX_AGGS = 100;

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
    // parse meta
    state.isPending = false;
    state.total = action.payload.total;
    // parse aggregations
    state.aggregations = action.payload.aggregations.map( d => {
      let _values = d.values.splice(0, MAX_AGGS).map( _d => {
        let currentValue = action.queryObject[d.key];
        let _isActive;
        // look at array fields differently
        if (typeof currentValue === 'object') { 
          _isActive = (currentValue.indexOf(_d.key) >= 0);
        } else {
          _isActive = _d.key === currentValue;
        }
        return {
          name: _d.key,
          displayName: _d.key,
          key: _d.key,
          total: _d.total,
          isActive: _isActive
        };
      });
      return {
        name: d.key,
        displayName: d.key,
        key: d.key,
        values: _values
      };
    });
    // parse results
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
