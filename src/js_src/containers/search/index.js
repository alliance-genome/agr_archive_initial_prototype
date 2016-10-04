import React, { Component } from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';
import { DropdownButton, MenuItem } from 'react-bootstrap';

import style from './style.css';
import ResultsList from './resultsList';
import ResultsTable from './resultsTable';

import { SMALL_COL_CLASS, LARGE_COL_CLASS } from '../../constants';

class SearchComponent extends Component {
  renderResultsNode() {
    if (this.props.isTable) {
      return <ResultsTable entries={this.props.results} />;
    }
    return <ResultsList entries={this.props.results} />;
  }

  render() {
    const listHref = '/search?mode=list';
    const tableHref = '/search?mode=table';
    return (
      <div className={style.root}>
        <div className='row'>
          <div className={SMALL_COL_CLASS}>
            <p className={style.filterLabel}>Categories</p>
            <ul className='nav nav-pills nav-stacked'>
              <li className='nav-item'>
                <a className='nav-link active'>Genes (5)</a>
              </li>
              <li className='nav-item'>
                <a className='nav-link'>Diseases (3)</a>
              </li>
              <li className='nav-item'>
                <a className='nav-link'>Ortholog Groups (3)</a>
              </li>
            </ul>
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
  isTable: React.PropTypes.bool,
  query: React.PropTypes.string,
  results: React.PropTypes.array,
  total: React.PropTypes.number
};

function mapStateToProps(state) {
  let query = state.routing.locationBeforeTransitions.query;
  let _isTable = (query.mode === 'table');
  return {
    isTable: _isTable,
    query: query.q,
    results: state.search.results,
    total: 5
  };
}

export { SearchComponent as SearchComponent };
export default connect(mapStateToProps)(SearchComponent);
