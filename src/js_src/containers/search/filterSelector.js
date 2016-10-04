import React, { Component } from 'react';
import { connect } from 'react-redux';

import style from './style.css';

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
      return (
        <li className='nav-item' key={_key}>
          <a className={`nav-link${classSuffix}`}>{nameNode} ({d.total})</a>
        </li>
      );
    });
  }

  renderFilters() {
    return this.props.aggregations.map( d => {
      return (
        <div className={style.aggValContainer} key={`filter${d.name}`}>
          <p className={style.filterLabel}>{d.displayName}</p>
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
};

function mapStateToProps(state) {
  return {
    activeCategory:  state.search.activeCategory,
    aggregations: state.search.aggregations,
  };
}

export { FilterSelectorComponent as FilterSelectorComponent };
export default connect(mapStateToProps)(FilterSelectorComponent);
