import React, { Component } from 'react';
import { Typeahead } from 'react-typeahead';

import style from './style.css';

class SearchBar extends Component {
  handleSubmit(e) {
    e.preventDefault();
  }

  render() {
    return (
      <div className={style.container}>
        <form onSubmit={this.handleSubmit}>
          <Typeahead
            className={style.typeahead}
            options={[]}
          />
        </form>
        <span className={style.searchIcon}><i className='fa fa-search' /></span>
      </div>
    );
  }
}

export default SearchBar;
