import React, { Component, PropTypes } from 'react';
import { Link } from 'react-router';
import style from './style.css';
import logo from './agr_logo.png';

class Layout extends Component {
  render() {
    return (
      <div className={style.appContainer}>
        <div className={style.topHeader}>
          <Link to='/'>
            <img src={logo} />
          </Link>
        </div>
        <nav className={`navbar navbar-light bg-faded ${style.midHeader}`}>
          <ul className='nav navbar-nav'>
            <li className='nav-item active'>
              <Link className={`nav-link ${style.navLink}`} to='/'>{'Home'}</Link>
            </li>
            <li className='nav-item active'>
              <Link className={`nav-link ${style.navLink}`} to='/about'>{'About'}</Link>
            </li>
            <li className='nav-item active'>
              <Link className={`nav-link ${style.navLink}`} to='/search'>{'Search'}</Link>
            </li>
          </ul>
        </nav>
        <div className={style.contentContainer}>
          {this.props.children}
        </div>
        <footer className={style.footer}>
          <p>&copy; 2016 Alliance of Genome Resources</p>
        </footer>
      </div>
    );
  }
}

Layout.propTypes = {
  children: PropTypes.node
};

export default Layout;
