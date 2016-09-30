import React, { Component } from 'react';
import { connect } from 'react-redux';

import style from './style.css';
import Table from '../../components/table';

class SearchComponent extends Component {
  render() {
    return (
      <div className={style.root}>
        <div className='row'>
          <div className={`col-sm-2 ${style.filterContainer}`}>
            <p className={style.filterLabel}>Categories</p>
            <ul className='nav nav-pills nav-stacked'>
              <li className='nav-item'>
                <a className='nav-link active'>Genes (3)</a>
              </li>
              <li className='nav-item'>
                <a className='nav-link'>Diseases (1)</a>
              </li>
              <li className='nav-item'>
                <a className='nav-link'>Ortholog Groups (1)</a>
              </li>
            </ul>
          </div>
          <div className='col-sm-9'>
            <p>99 results for "lorem"</p>
            <label>Genes</label>
            <Table entries={this.props.results} />
          </div>
        </div>
      </div>
    );
  }
}

function mapStateToProps(state) {
  return {
    results: state.search.results
  };
}

export { SearchComponent as SearchComponent };
export default connect(mapStateToProps)(SearchComponent);
