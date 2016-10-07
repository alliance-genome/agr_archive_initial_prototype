import React, { Component } from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';
import { DropdownButton, MenuItem } from 'react-bootstrap';

import { getQueryParamWithValueChanged } from '../../lib/searchHelpers';

import style from './style.css';

class SearchControlsComponent extends Component {
  render() {
    let listQp = getQueryParamWithValueChanged('mode', 'list', this.props.queryParams);
    let tableQp = getQueryParamWithValueChanged('mode', 'table', this.props.queryParams);
    let listHref = { pathname: '/search', query: listQp };
    let tableHref = { pathname: '/search', query: tableQp };
    return (
      <div>
        <div className={`btn-group ${style.control}`} role='group'>
          <Link className={`btn btn-${!this.props.isTable ? 'primary': 'secondary'}`} to={listHref}><i className='fa fa-list' /> List</Link>
          <Link className={`btn btn-${this.props.isTable ? 'primary': 'secondary'}`} to={tableHref}><i className='fa fa-table' /> Table</Link>
        </div>
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
      </div>
    );
  }
}

SearchControlsComponent.propTypes = {
  currentPage: React.PropTypes.number,
  isTable: React.PropTypes.bool,
  queryParams: React.PropTypes.object,
  totalPages: React.PropTypes.number
};

function mapStateToProps(state) {
  let location = state.routing.locationBeforeTransitions;
  let _queryParams = location ? state.routing.locationBeforeTransitions.query : {};
  let _isTable = (_queryParams.mode === 'table');
  return {
    currentPage: 1,
    isTable: _isTable,
    queryParams: _queryParams,
    totalPages: 5
  };
}

export { SearchControlsComponent as SearchControlsComponent };
export default connect(mapStateToProps)(SearchControlsComponent);
