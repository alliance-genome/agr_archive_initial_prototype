import React, { Component } from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';

import style from './style.css';
import { getQueryParamWithValueChanged } from '../../lib/searchHelpers';

import { selectTotal } from '../../selectors/searchSelectors.js';

const IGNORED_PARAMS = ['page', 'mode'];
const SORT_PRIORITY = ['category', 'q'];

class SearchBreadcrumbsComponent extends Component {
  renderCrumbValues(key, values) {
    return values.map( (d, i) => {
      let newQp = getQueryParamWithValueChanged(key, d, this.props.queryParams);
      let newPath = { pathname: '/search', query: newQp };
      let label = (key === 'q') ? `"${d}"` : d;
      return (
        <Link className={`btn btn-primary ${style.sortLabel}`} key={`bc${key}.${i}`} to={newPath}><span>{label} <i className='fa fa-times' /></span></Link>
      );
    });
  }

  renderCrumbs() {
    let qp = this.props.queryParams;
    let keys = Object.keys(qp).filter( d => IGNORED_PARAMS.indexOf(d) < 0);
    // make sure they are sorted
    keys = keys.sort( (a, b) => (SORT_PRIORITY.indexOf(a) < SORT_PRIORITY.indexOf(b)) );
    return keys.map( d => {
      let values = qp[d];
      if (typeof values !== 'object') values = [values];
      return this.renderCrumbValues(d, values);
    });
  }

  render() {
    return (
      <div>
        <p>{this.props.total.toLocaleString()} results for {this.renderCrumbs()}</p>
      </div>
    );
  }
}

SearchBreadcrumbsComponent.propTypes = {
  queryParams: React.PropTypes.object,
  total: React.PropTypes.number
};

function mapStateToProps(state) {
  let location = state.routing.locationBeforeTransitions;
  let _queryParams = location ? state.routing.locationBeforeTransitions.query : {};
  return {
    queryParams: _queryParams,
    total: selectTotal(state)
  };
}

export { SearchBreadcrumbsComponent as SearchBreadcrumbsComponent };
export default connect(mapStateToProps)(SearchBreadcrumbsComponent);
