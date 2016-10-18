/*eslint-disable no-case-declarations */
import { fromJS } from 'immutable';

import { parseAggs, parseResults } from './searchParsers';

const DEFAULT_PAGE_SIZE = 50;
const DEFAULT_STATE = fromJS({
  activeCategory: 'none',
  aggregations: [],
  errorMessage: '',
  isError: false,
  isPending: false,
  pageSize: DEFAULT_PAGE_SIZE,
  // for multi table
  geneResults: [],
  goResults: [],
  diseaseResults: [],
  orthoGroupResults: [],
  geneTotal: 0,
  goTotal: 0,
  diseaseTotal: 0,
  orthoGroupTotal: 0,
  // mixed
  results: [],
  total: 0,
});

const searchReducer = function (state = DEFAULT_STATE, action) {
  //TODO cleanup fromJS/toJS handling here.
  switch(action.type) {
  case 'SEARCH_ERROR':
    if (!action.payload) {
      return state.set('errorMessage', '').set('isError', false);
    }
    return state.set('errorMessage', action.payload).set('isError', true);
  case 'SEARCH_SET_PENDING':
    return state.set('isPending', action.payload);
  case '@@router/LOCATION_CHANGE':
    // update active cat
    let newActiveCat = action.payload.query.category || 'none';
    // parse aggs to update active state during route change
    return state.set('aggregations', fromJS(parseAggs(state.get('aggregations').toJS(), action.payload.query)))
                .set('activeCategory', newActiveCat);
  case 'SEARCH_RESPONSE':
    // parse meta
    return state
      .set('isPending',false)
      .set('total', action.payload.total)
      // parse aggregations
      .set('aggregations', fromJS(parseAggs(action.payload.aggregations, action.queryParams))) 
      // parse results
      .set('results', fromJS(parseResults(action.payload.results)));
  default:
    return state;
  }
};

export default searchReducer;
