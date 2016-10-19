import React, { Component } from 'react';

import style from './style.css';

class Loader extends Component {
  render() {
    return (
      <div className={style.loaderContainer}>
        <div className={style.loader} />
      </div>
    );
  }
}

export default Loader;
