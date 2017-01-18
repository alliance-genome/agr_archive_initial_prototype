export function clearError () {
  return {
    type: 'SEARCH_ERROR',
    payload: false
  };
}

export function receiveResponse (response, _queryParams) {
  return {
    type: 'SEARCH_RESPONSE',
    payload: response,
    queryParams: _queryParams
  };
}

export function setError (message) {
  return {
    type: 'SEARCH_ERROR',
    payload: message
  };
}

export function setPending (isPending) {
  return {
    type: 'SEARCH_SET_PENDING',
    payload: isPending
  };
}
