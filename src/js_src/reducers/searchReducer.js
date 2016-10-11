/*eslint-disable no-case-declarations */
import { fromJS } from 'immutable';

import { injectHighlightIntoResponse } from '../lib/searchHelpers';

const DEFAULT_PAGE_SIZE = 50;
const DEFAULT_STATE = fromJS({
  activeCategory: 'none',
  aggregations: [],
  errorMessage: '',
  isError: false,
  isPending: false,
  pageSize: DEFAULT_PAGE_SIZE,
  results: [],
  total: 0,
});

const searchReducer = function (state = DEFAULT_STATE, action) {
  //TODO cleanup fromJS/toJS handling here.
  switch(action.type) {
  case 'SEARCH_ERROR':
    return state.set('errorMessage', action.payload).set('isError',true);
  case '@@router/LOCATION_CHANGE':
    // update active cat
    let newActiveCat = action.payload.query.category || 'none';
    // parse aggs to update active state during route change
    return state.set('aggregations', fromJS(parseAggs(state.get('aggregations').toJS(), action.payload.query)))
                .set('activeCategory', newActiveCat);
  case 'SEARCH_RESPONSE':
    // parse meta
    return state.set('isPending',false)
                .set('total', action.payload.total)
                // parse aggregations
                .set('aggregations', fromJS(parseAggs(action.payload.aggregations, action.queryObject))) 
                // parse results
                .set('results',fromJS(action.payload.results.map( _d => { 
                  let d = injectHighlightIntoResponse(_d);
                  return {
                    symbol: d.symbol,
                    name: d.name,
                    geneId: 'ID:12345678',
                    sourceHref: d.href,
                    synonyms: d.synonym,
                    geneType: d.type,
                    genomicStartCoordinates: '',
                    genomicStopCoordinates: '',
                    relativeStartCoordinates: '',
                    relativeStopCoordinates: '',
                    species: d.organism,
                    highlight: d.highlights
                  };
                })));
  default:
    return state;
  }
};

function parseAggs(rawAggs, queryObject) {
  return rawAggs.map( d => {
    let _values = d.values.map( _d => {
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
