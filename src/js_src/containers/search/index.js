/*eslint-disable no-undef */
import React, { Component } from 'react';
import { connect } from 'react-redux';

import style from './style.css';
import FilterSelector from './filterSelector';
import SearchBreadcrumbs from './searchBreadcrumbs';
import SearchControls from './searchControls';
import ResultsList from './resultsList';
import ResultsTable from './resultsTable';
import { SMALL_COL_CLASS, LARGE_COL_CLASS, SEARCH_API_ERROR_MESSAGE } from '../../constants';
import { receiveResponse, setError } from './searchActions';

const BASE_SEARCH_URL = '/api/search';

class SearchComponent extends Component {
  // fetch data at start
  componentDidMount() {
    this.fetchData();
  }

  // fetch data whenever URL changes within /search
  componentDidUpdate (prevProps) {
    if (prevProps.location !== this.props.location) {
      this.fetchData();
    }
  }

  fetchData() {
    let searchUrl = BASE_SEARCH_URL + this.props.location.search;
    // depends on global $
    $.ajax({
      url : searchUrl,
      type : 'GET',
      dataType:'json',
      success: data => {              
        this.props.dispatch(receiveResponse(data, this.props.location));
      },
      error: (request, e) => {
        if (process.env.NODE_ENV === 'production') {
          this.props.dispatch(setError(SEARCH_API_ERROR_MESSAGE));
        } else {
          throw(e);
        }
      }
    });
  }

  renderResultsNode() {
    if (this.props.isTable) {
      return <ResultsTable entries={this.props.results} />;
    }
    return <ResultsList entries={this.props.results} />;
  }

  renderErrorNode() {
    if (!this.props.isError) {
      return null;
    }
    return (
      <div className='alert alert-warning'>
        <h3>Oops, Error</h3>
        <p>{this.props.errorMessage}</p>
      </div>
    );
  }

  render() {
    return (
      <div className={style.root}>
        {this.renderErrorNode()}
        <div className='row'>
          <div className={SMALL_COL_CLASS}>
            <FilterSelector />
          </div>
          <div className={LARGE_COL_CLASS}>
            <SearchBreadcrumbs />
            <SearchControls />
            {this.renderResultsNode()}
          </div>
        </div>
      </div>
    );
  }
}

SearchComponent.propTypes = {
  dispatch: React.PropTypes.func,
  errorMessage: React.PropTypes.string,
  history: React.PropTypes.object,
  isError: React.PropTypes.bool,
  isTable: React.PropTypes.bool,
  location: React.PropTypes.object,
  results: React.PropTypes.array,
};

function mapStateToProps(state) {
  let _location = state.routing.locationBeforeTransitions;
  let query = _location.query;
  let _isTable = (query.mode === 'table');
  return {
    errorMessage: state.search.errorMessage,
    isError: state.search.isError,
    isTable: _isTable,
    location: _location,
    results: state.search.results,
  };
}

export { SearchComponent as SearchComponent };
export default connect(mapStateToProps)(SearchComponent);
