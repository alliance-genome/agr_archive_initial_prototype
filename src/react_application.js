import React from 'react';
import { BrowserRouter, Match, MemoryRouter } from 'react-router';

import About from './components/about';
import Home from './components/home';
import Layout from './components/layout';
import Search from './components/search';

const App = () => {
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
};

export default App;
