import React from 'react';
import { BrowserRouter, Match } from 'react-router';

import About from './components/about';
import Home from './components/home';
import Layout from './components/layout';
import Search from './components/search';

const App = () => {
  return (
    <BrowserRouter>
      <Layout>
        <Match component={Home} exactly pattern='/' />
        <Match component={About} pattern='/about' />
        <Match component={Search} pattern='/search' />
      </Layout>
    </BrowserRouter>
  );
};

export default App;
