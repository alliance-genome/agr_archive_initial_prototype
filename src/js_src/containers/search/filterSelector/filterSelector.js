import React, { Component } from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';

import style from './style.css';
import SingleFilterSelector from './singleFilterSelector';
import { getQueryParamWithValueChanged } from '../../../lib/searchHelpers';

import {
  selectActiveCategory,
  selectAggregations
} from '../../../selectors/searchSelectors';

class FilterSelectorComponent extends Component {
  renderFilters() {
    let aggs = this.props.aggregations;
    if (aggs.length === 0) {
      return <p>No filters available.</p>;
    }
    return aggs.map( d => {
      return <div key={`filter${d.name}`}><SingleFilterSelector {...d} queryParams={this.props.queryParams} /></div>;
    });
  }

  renderCatSelector() {
    let cat = this.props.activeCategory;
    if (cat === 'none') {
      return null;
    }
    let newQp = getQueryParamWithValueChanged('category', [], this.props.queryParams, true);
    let newHref = { pathname: '/search', query: newQp };
    return (
      <div>
          <h5>Category: {this.props.activeCategory}</h5>
        <p>
          <Link to={newHref}><i className='fa fa-chevron-left' /> Show all Categories</Link>
        </p>
      </div>
    );
  }

  render() {
    return (
      <div className={style.aggContainer} >
        {this.renderCatSelector()}
        {this.renderFilters()}
      </div>
    );
  }
}

FilterSelectorComponent.propTypes = {
  activeCategory: React.PropTypes.string,
  aggregations: React.PropTypes.array,
  queryParams: React.PropTypes.object
};

function mapStateToProps(state) {
  let location = state.routing.locationBeforeTransitions;
  let _queryParams = location ? location.query : {};
  return {
    activeCategory:  selectActiveCategory(state),
    aggregations: selectAggregations(state),
    queryParams: _queryParams
  };
}

export { FilterSelectorComponent as FilterSelectorComponent };
export default connect(mapStateToProps)(FilterSelectorComponent);
