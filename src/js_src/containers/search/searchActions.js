export function receiveResponse (response) {
  return {
    type: 'SEARCH_RESPONSE',
    payload: response
  };
}

export function setError (message) {
  return {
    type: 'SEARCH_ERROR',
    payload: message
  };
}
