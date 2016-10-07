// import _ from 'underscore';

import { injectHighlightIntoResponse } from '../lib/searchHelpers';

import { fromJS } from 'immutable';

const MAX_AGGS = 50;

const DEFAULT_STATE = fromJS({
  activeCategory: 'none',
  aggregations: [],
  errorMessage: '',
  isError: false,
  isPending: false,
  results: [],
  total: 0,
});

const searchReducer = function (state = DEFAULT_STATE, action) {
    switch(action.type) {
        case 'SEARCH_ERROR':
            return state.set('errorMessage', action.payload).set('isError',true);
        case '@@router/LOCATION_CHANGE':
            // parse aggs to update active state during route change
            return state.set('aggregations', parseAggs(state.aggregations, action.payload.query));
        case 'SEARCH_RESPONSE':
            // parse meta
            return state.set('isPending',false)
                        .set('total', action.payload.total) 
                        // parse aggregations
                        .set('aggregations', parseAggs(action.payload.aggregations, action.queryObject)) 
                        // parse results
                        .set('results',action.payload.results.map( _d => { 
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
                        }));
        default:
            return state;
    }
};

function parseAggs(rawAggs, queryObject) {
  return rawAggs.map( d => {
    let _values = d.values.splice(0, MAX_AGGS).map( _d => {
      let currentValue = queryObject[d.key];
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
}

export default searchReducer;
