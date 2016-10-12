export function clearError () {
  return {
    type: 'SEARCH_ERROR',
    payload: false
  };
}

export function receiveResponse (response, locationObj) {
  return {
    type: 'SEARCH_RESPONSE',
    payload: response,
    queryObject: locationObj.query
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
