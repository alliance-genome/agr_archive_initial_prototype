import fetch from 'isomorphic-fetch';

const API_BASE = '/api/search';

export function fetchData() {
  return function (dispatch, getState) {
    let state = getState();
    let queryString = state.routing.locationBeforeTransitions.search;
    let searchUrl = API_BASE + queryString;
    fetch(searchUrl)
      .then(function(response) {
        if (response.status >= 400) {
          throw new Error('API error.');
        }
        let responseAction = receiveResponse(response.json());
        dispatch(receiveResponse(responseAction));
      });
  };
}

export function receiveResponse (response) {
  return {
    type: 'SEARCH_RESPONSE',
    payload: response
  };
}
