import React from 'react';
import { IndexRoute, Route  } from 'react-router';

import About from './containers/about';
import Help from './containers/help';
import Home from './containers/home';
import Layout from './containers/layout';
import Search from './containers/search';

export default (
  <Route component={Layout} path='/'>
    <IndexRoute component={Home} />
    <Route component={About} path='about' />
    <Route component={Help} path='help' />
    <Route component={Search} path='search' />
  </Route>
);
