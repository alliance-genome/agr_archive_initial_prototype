/*eslint-disable no-undef */
import React, { Component } from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';
import { DropdownButton, MenuItem } from 'react-bootstrap';

import style from './style.css';
import FilterSelector from './filterSelector';
import ResultsList from './resultsList';
import ResultsTable from './resultsTable';
import { SMALL_COL_CLASS, LARGE_COL_CLASS, SEARCH_API_ERROR_MESSAGE } from '../../constants';
import { getQueryParamWithValueChanged } from '../../lib/searchHelpers';
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
    let listQp = getQueryParamWithValueChanged('mode', 'list', this.props.location);
    let tableQp = getQueryParamWithValueChanged('mode', 'table', this.props.location);
    let listHref = { pathname: '/search', query: listQp };
    let tableHref = { pathname: '/search', query: tableQp };
    return (
      <div className={style.root}>
        {this.renderErrorNode()}
        <div className='row'>
          <div className={SMALL_COL_CLASS}>
            <FilterSelector />
          </div>
          <div className={LARGE_COL_CLASS}>
            <div>
              <div className={style.controlContainer}>
              <label className={style.sortLabel}>Page 1 of 1</label>
              <div className={`btn-group ${style.control}`} role='group'>
                <button className='btn btn-secondary'><i className='fa fa-chevron-left' /></button>
                <button className='btn btn-secondary'><i className='fa fa-chevron-right' /></button>
              </div>
              <label className={style.sortLabel}>Sort By</label>
                <DropdownButton className={`btn-secondary ${style.control}`} id='bg-nested-dropdown' title='Relevance'>
                  <MenuItem eventKey='1'>Dropdown link</MenuItem>
                  <MenuItem eventKey='2'>Dropdown link</MenuItem>
                </DropdownButton>
                <a className={`btn btn-secondary ${style.agrDownloadBtn}`}><i className='fa fa-download' /> Download</a>
              </div>
              <p>{this.props.total.toLocaleString()} results for "{this.props.query}"</p>
            </div>
            <ul className='nav nav-tabs'>
              <li className='nav-item'>
                <Link className={`nav-link${!this.props.isTable ? ' active': ''}`} to={listHref}><i className='fa fa-list' /> List</Link>
              </li>
              <li className='nav-item'>
                <Link className={`nav-link${this.props.isTable ? ' active': ''}`} to={tableHref}><i className='fa fa-table' /> Table</Link>
              </li>
            </ul>
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
  query: React.PropTypes.string,
  results: React.PropTypes.array,
  total: React.PropTypes.number
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
    query: query.q,
    results: state.search.results,
    total: state.search.total
  };
}

export { SearchComponent as SearchComponent };
export default connect(mapStateToProps)(SearchComponent);
