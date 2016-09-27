import React, { Component, PropTypes } from 'react';
import { Link } from 'react-router';
import style from './style.css';

class App extends Component {
  render() {
    return (
        <div className={style.root}>
            <nav className='navbar navbar-static-top navbar-light bg-faded'>
                <Link className='navbar-brand' to='/'>{'AGR'}</Link>
                <ul className='nav navbar-nav'>
                    <li className='nav-item active'>
                        <Link className='nav-link' to='/'>{'Home'}</Link>
                    </li>
                    <li className='nav-item active'>
                        <Link className='nav-link' to='/about'>{'About'}</Link>
                    </li>
                    <li className='nav-item active'>
                        <Link className='nav-link' to='/search'>{'Search'}</Link>
                    </li>
                </ul>
            </nav>
            <div className='container'>
                {this.props.children}
            </div>
            <footer>
              <p>&copy; 2016 Company, Inc.</p>
            </footer>
        </div>
    );
  }
}

App.propTypes = {
  children: PropTypes.node
};

export default App;
