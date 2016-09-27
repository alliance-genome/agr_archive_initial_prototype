import React from 'react';
import { render } from 'react-dom';
import { Router, Route, browserHistory } from 'react-router';

import About from './components/about';
import App from './components/app';
import Search from './components/search';

render((
    <Router history={browserHistory}>
        <Route component={App} path='/'>
            <Route component={About} path='/about' />
            <Route component={Search} path='/search' />
        </Route>       
    </Router>
), document.getElementById('app'));
