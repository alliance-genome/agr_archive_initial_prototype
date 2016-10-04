import React, { Component, PropTypes } from 'react';
import { Link } from 'react-router';

import SearchBar from './searchBar';
import style from './style.css';
import logo from './agrLogo.png';

class Layout extends Component {
  render() {
    return (
      <div className={style.appContainer}>
        <div className={`alert alert-info ${style.appAlert}`} role='alert'>
          This website is a prototype and information may not be verified.
        </div>
        <div className={style.topHeader}>
          <div className='row'>
            <div className='col-sm-2'>
              <Link to='/'>
                <img className={style.logo} src={logo} />
              </Link>
            </div>
            <div className='col-sm-10' />
          </div>
        </div>
        <nav className={`navbar navbar-light bg-faded ${style.midHeader}`}>
          <div className='row'>
            <div className='col-sm-2'>
              <div className={style.nav}>
                <Link className={`nav-link ${style.navLink}`} to='/'><i className='fa fa-home' /> Home</Link>
                <Link className={`nav-link ${style.navLink}`} to='/about'><i className='fa fa-info-circle' /> About</Link>
                <Link className={`nav-link ${style.navLink}`} to='/help'><i className='fa fa-question-circle' /> Help</Link>
              </div>
            </div>
            <div className='col-sm-10'>
              <SearchBar />
            </div>
          </div>
        </nav>
        <div className={style.contentContainer}>
          {this.props.children}
        </div>
      </div>
    );
  }
}

Layout.propTypes = {
  children: PropTypes.node
};

export default Layout;
