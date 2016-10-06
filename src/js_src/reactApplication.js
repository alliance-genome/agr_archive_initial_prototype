import React, { Component } from 'react';
import { Router, browserHistory, createMemoryHistory, IndexRoute, Route  } from 'react-router';
import { Provider } from 'react-redux';
import { syncHistoryWithStore } from 'react-router-redux';
import configureStore from './lib/configureStore';

import About from './containers/about';
import Home from './containers/home';
import Layout from './containers/layout';
import Search from './containers/search';

class ReactApp extends Component {
  render() {
    let isBrowser = typeof window === 'object';
    let historyObj = isBrowser ? browserHistory : createMemoryHistory('/');
    let store = configureStore(historyObj);
    let history = syncHistoryWithStore(historyObj, store);
    return (
      <Provider store={store}>
        <Router history={history}>
          <Route component={Layout} path='/'>
            <IndexRoute component={Home} />
            <Route component={About} path='about' />
            <Route component={Search} path='search' />
          </Route>
        </Router>
      </Provider>
    );
  }
}

export default ReactApp;
