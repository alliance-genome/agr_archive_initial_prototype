import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Typeahead } from 'react-typeahead';
import { push } from 'react-router-redux';

import style from './style.css';

class SearchBarComponent extends Component {
  handleSubmit(e) {
    e.preventDefault();
    this.props.dispatch(push('/search'));
  }

  render() {
    return (
      <div className={style.container}>
        <form onSubmit={this.handleSubmit.bind(this)}>
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
