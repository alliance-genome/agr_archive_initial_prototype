import React, { Component } from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';

import style from './style.css';
import Table from '../../components/table';
import ResultsList from './resultsList';

class SearchComponent extends Component {
  renderResultsNode() {
    if (this.props.isTable) {
      return <Table entries={this.props.results} />;
    }
    return <ResultsList entries={this.props.results} />;
  }

  render() {
    const listHref = '/search?mode=list';
    const tableHref = '/search?mode=table';
    return (
      <div className={style.root}>
        <div className='row'>
          <div className={`col-sm-2 ${style.filterContainer}`}>
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
          <div className='col-sm-9'>
            <p>5 results for "{this.props.query}"</p>
            <a className={`btn btn-sm btn-secondary ${style.agrDownloadBtn}`}><i className='fa fa-download' /> Download</a>
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
  results: React.PropTypes.array
};

function mapStateToProps(state) {
  let query = state.routing.locationBeforeTransitions.query;
  let _isTable = (query.mode === 'table');
  return {
    isTable: _isTable,
    query: query.q,
    results: state.search.results
  };
}

export { SearchComponent as SearchComponent };
export default connect(mapStateToProps)(SearchComponent);
