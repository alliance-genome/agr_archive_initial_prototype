import React, { Component } from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';

import style from './style.css';
import { getQueryParamWithValueChanged } from '../../lib/searchHelpers';

class FilterSelectorComponent extends Component {
  renderFilterValues(filterObj) {
    let values = filterObj.values;
    return values.map( d => {
      let classSuffix = d.isActive ? ' active' : '';
      let _key = `fv.${filterObj.name}.${d.name}`;
      let nameNode;
      if (filterObj.name === 'species') {
        nameNode = <i>{d.displayName}</i>;
      } else {
        nameNode = <span>{d.displayName}</span>;
      }
      let newQueryObj = getQueryParamWithValueChanged(filterObj.key, d.key, this.props.location.query);
      return (
        <li className='nav-item' key={_key}>
          <Link className={`nav-link${classSuffix}`} to={{ pathname: '/search', query: newQueryObj }}>{nameNode} ({d.total})</Link>
        </li>
      );
    });
  }

  renderFilters() {
    let aggs = this.props.aggregations;
    if (aggs.length === 0) {
      return <p>No filters available.</p>;
    }
    return aggs.map( d => {
      return (
        <div className={style.aggValContainer} key={`filter${d.name}`}>
          <p className={style.filterLabel}><b>{d.displayName}</b></p>
          <ul className='nav nav-pills nav-stacked'>
            {this.renderFilterValues(d)}
          </ul>
        </div>
      );
    });
  }

  renderCatSelector() {
    let cat = this.props.activeCategory;
    if (cat === 'none') {
      return null;
    }
    return (
      <div>
         <h5>Category: {this.props.activeCategory}</h5>
        <p>
          <a href='#'><i className='fa fa-chevron-left' /> Show all Categories</a>
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
  dispatch: React.PropTypes.func,
  location: React.PropTypes.object
};

function mapStateToProps(state) {
  return {
    activeCategory:  state.search.activeCategory,
    aggregations: state.search.aggregations,
    location: state.routing.locationBeforeTransitions
  };
}

export { FilterSelectorComponent as FilterSelectorComponent };
export default connect(mapStateToProps)(FilterSelectorComponent);
