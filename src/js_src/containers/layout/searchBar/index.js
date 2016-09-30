import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Typeahead } from 'react-typeahead';
import { push } from 'react-router-redux';

import style from './style.css';

const INPUT_CLASS = 'agr-search-input';

class SearchBarComponent extends Component {
  handleSubmit(e) {
    e.preventDefault();
    let query = this.getQuery();
    this.props.dispatch(push({ pathname: '/search', query: { q: query } }));
  }

  getQuery() {
    let el = document.getElementsByClassName(INPUT_CLASS)[0];
    return el.value;
  }

  render() {
    return (
      <div className={style.container}>
        <form onSubmit={this.handleSubmit.bind(this)}>
          <Typeahead
            className={style.typeahead}
            customClasses={{ input: INPUT_CLASS }}
            options={[]}
          />
        </form>
        <span className={style.searchIcon}><i className='fa fa-search' /></span>
      </div>
    );
  }
}

SearchBarComponent.propTypes = {
  dispatch: React.PropTypes.func,
  query: React.PropTypes.string
};

function mapStateToProps() {
  return {
  };
}

export { SearchBarComponent as SearchBarComponent };
export default connect(mapStateToProps)(SearchBarComponent);
