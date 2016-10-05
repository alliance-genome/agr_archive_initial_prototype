import React, { Component } from 'react';
import { Router, browserHistory, createMemoryHistory, IndexRoute, Route  } from 'react-router';
import { Provider } from 'react-redux';
import { syncHistoryWithStore } from 'react-router-redux';
import configureStore from './lib/configureStore';

import About from './containers/about';
import Home from './containers/home';
import Layout from './containers/layout';
import Search from './containers/search';

import { SEARCH_API_ERROR_MESSAGE } from './constants';
import { receiveResponse, setError } from './containers/search/searchActions';

const BASE_SEACRCH_URL = '/api/search';

class ReactApp extends Component {
  render() {
    let isBrowser = typeof window === 'object';
    let historyObj = isBrowser ? browserHistory : createMemoryHistory('/');
    let store = configureStore(historyObj);
    let history = syncHistoryWithStore(historyObj, store);
    // fetch data when changing route within search or entering, defined here to properly follow pushState nav
    // dispatch needed actions
    function onSearchChange(prevState, nextState) {
      let location = nextState.location || prevState.location;
      let queryUrl = location.search;
      fetchSearchData(queryUrl).then( response => {
        store.dispatch(receiveResponse(response));
      }).catch( (e) => {
        if (process.env.NODE_ENV === 'production') {
          store.dispatch(setError(SEARCH_API_ERROR_MESSAGE));
        } else {
          throw(e);
        }
      });
    }
    return (
      <Provider store={store}>
        <Router history={history}>
          <Route component={Layout} path='/'>
            <IndexRoute component={Home} />
            <Route component={About} path='about' />
            <Route component={Search}  onChange={onSearchChange} onEnter={onSearchChange} path='search' />
          </Route>
        </Router>
      </Provider>
    );
  }
}

function fetchSearchData(queryUrl) {
  let searchUrl = BASE_SEACRCH_URL + queryUrl;
  return fetch(searchUrl)
    .then( (response) => {
      if (response.status >= 400) {
        throw new Error('API error.');
      }
      return response.json();
    });
}

export default ReactApp;
