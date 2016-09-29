import React, { Component } from 'react';
import { createStore, combineReducers } from 'redux';
import { Router, Route, browserHistory, IndexRoute, memoryHistory } from 'react-router';
import { syncHistoryWithStore, routerReducer } from 'react-router-redux';
import { Provider } from 'react-redux';

import About from './containers/about';
import Home from './containers/home';
import Layout from './containers/layout';
import Search from './containers/search';

// init redux store a la https://github.com/reactjs/react-router-redux
const reducers = combineReducers({
  routing: routerReducer
});
const store = createStore(reducers);
if (module.hot) {
  // Enable Webpack hot module replacement for reducers
  module.hot.accept('./reducers', () => {
    store.replaceReducer(reducers);
  });
}
let isBrowser = typeof window === 'object';
let historyObj = isBrowser ? browserHistory : memoryHistory;
let history = syncHistoryWithStore(historyObj, store);

console.log('fart');
class ReactApp extends Component {
  render() {
    return (
      <Provider store={store}>
        <Router history={history}>
          <Route component={Layout} path='/'>
            <IndexRoute component={Home} />
            <Route component={About} path='/about' />
            <Route component={Search} path='/search' />
          </Route>
        </Router>
      </Provider>
    );
  }
}

export default ReactApp;
