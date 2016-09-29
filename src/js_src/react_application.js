import React, { Component } from 'react';
import { createStore, combineReducers } from 'redux';
import { Match, MemoryRouter } from 'react-router';
import { ConnectedRouter, routerReducer } from 'react-router-redux';
import { Provider } from 'react-redux';

import About from './containers/about';
import Home from './containers/home';
import Layout from './containers/layout';
import Search from './containers/search';

// init redux store a la https://github.com/reactjs/react-router-redux
let store = createStore(
  combineReducers({
    router: routerReducer
  })
);

class ReactApp extends Component {
  render() {
    let layoutNode = (
      <Layout>
        <Match component={Home} exactly pattern='/' />
        <Match component={About} pattern='/about' />
        <Match component={Search} pattern='/search' />
      </Layout>
    );
    let isBrowser = typeof window === 'object';
    let routerNode = isBrowser ? <ConnectedRouter>{layoutNode}</ConnectedRouter> :  <MemoryRouter>{layoutNode}</MemoryRouter>;
    return (
      <Provider store={store}>
        {routerNode}
      </Provider>
    );
  }
}

export default ReactApp;
