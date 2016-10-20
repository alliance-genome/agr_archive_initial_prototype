/*eslint-disable react/no-set-state */
import React, { Component } from 'react';
import { Link } from 'react-router';

import style from './style.css';
import { getQueryParamWithValueChanged } from '../../../lib/searchHelpers';
import CategoryLabel from '../categoryLabel';

const SMALL_NUM_VISIBLE = 5;
const MED_NUM_VISIBLE = 20;
const MAX_NUM_VISIBLE = 1000;

class SingleFilterSelector extends Component {
  constructor(props) {
    super(props);
    this.state = {
      numVisible: SMALL_NUM_VISIBLE
    };
  }

  renderFilterValues() {
    let values = this.props.values.slice(0, this.state.numVisible);
    return values.map( d => {
      let classSuffix = d.isActive ? ' active' : '';
      let _key = `fv.${this.props.name}.${d.name}`;
      let nameNode;
      if (this.props.name.match('species')) {
        nameNode = <i>{d.displayName}</i>;
      } else if (this.props.name === 'category') {
        nameNode = <CategoryLabel category={d.name} />;
      } else {
        nameNode = <span>{d.displayName}</span>;
      }
      let newQueryObj = getQueryParamWithValueChanged(this.props.name, d.key, this.props.queryParams);
      return (
        <li className='nav-item' key={_key}>
          <Link className={`nav-link${classSuffix}`} to={{ pathname: '/search', query: newQueryObj }}>
            <span className={style.aggLink}>
              <span className={style.aggLinkLabel}>{nameNode}</span><span>{d.total.toLocaleString()}</span>
            </span>
          </Link>
        </li>
      );
    });
  }

  handleControlClick(e) {
    e.preventDefault();
    this.setState({ numVisible: this.getNextNumVisible() });
  }

  getNextNumVisible() {
    let currentNum = this.state.numVisible;
    let newNum;
    if (currentNum === SMALL_NUM_VISIBLE) {
      newNum = MED_NUM_VISIBLE;
    } else if (currentNum === MED_NUM_VISIBLE) {
      newNum = MAX_NUM_VISIBLE;
    } else {
      newNum = SMALL_NUM_VISIBLE;
    }
    return newNum;
  }

  renderControlNode() {
    if (this.props.values.length <= SMALL_NUM_VISIBLE) return null;
    let label = (this.state.numVisible !== MAX_NUM_VISIBLE) ? 'Show More' : `Show ${SMALL_NUM_VISIBLE}`;
    return (
      <p className='text-sm-right'>
        <a href='#' onClick={this.handleControlClick.bind(this)}>{label}</a>
      </p>
    );
  }

  render() {
    // don't render an empty filter
    if (this.props.values.length === 0) {
      return null;
    }
    return (
      <div className={style.aggValContainer}>
        <p className={style.filterLabel}><b>{this.props.displayName}</b></p>
        <ul className='nav nav-pills nav-stacked'>
          {this.renderFilterValues(this.props)}
        </ul>
        {this.renderControlNode()}
      </div>
    );
  }
}

SingleFilterSelector.propTypes = {
  displayName: React.PropTypes.string,
  name: React.PropTypes.string,
  queryParams: React.PropTypes.object,
  values: React.PropTypes.array
};

export default SingleFilterSelector;
