import React from 'react';
import { IndexRoute, Route } from 'react-router';

import About from './containers/about';
import Home from './containers/home';
import Layout from './containers/layout';
import Search from './containers/search';

const Routes = (
  <Route component={Layout} path='/'>
    <IndexRoute component={Home} />
    <Route component={About} path='about' />
    <Route component={Search} path='search' />
  </Route>
);

export default Routes;
