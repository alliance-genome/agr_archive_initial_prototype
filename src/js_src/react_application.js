import React, { Component } from 'react';

import { BrowserRouter, Match, MemoryRouter } from 'react-router';

import About from './containers/about';
import Home from './containers/home';
import Layout from './containers/layout';
import Search from './containers/search';

class ReactApp extends Component {
  render() {
    let layoutNode = (
      <Layout>
        <Match component={Home} exactly pattern='/' />
        <Match component={About} pattern='/about' />
        <Match component={Search} pattern='/search' />
      </Layout>
    );
    // use browser history if in the browser, otherwise use memory for history (like node or testing env)
    if (typeof window === 'object') {
      return <BrowserRouter>{layoutNode}</BrowserRouter>;
    }
    return <MemoryRouter>{layoutNode}</MemoryRouter>;
  }
}

export default ReactApp;
