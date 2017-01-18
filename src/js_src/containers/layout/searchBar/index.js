/*eslint-disable react/no-set-state */
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Typeahead } from 'react-typeahead';
import { push } from 'react-router-redux';
import { DropdownButton, MenuItem } from 'react-bootstrap';

import style from './style.css';
import CategoryLabel from '../../search/categoryLabel';

const INPUT_CLASS = 'agr-search-input';
const CATEGORY_OPTIONS = [
  {
    name: 'all',
    displayName: 'All'
  },
  {
    name: 'gene',
    displayName: 'Genes'
  },
  {
    name: 'go',
    displayName: 'Gene Ontology'
  },
  {
    name: 'disease',
    displayName: 'Diseases'
  },
  {
    name: 'ortholog group',
    displayName: 'Ortholog Groups'
  }
];
const DEFAULT_CAT = CATEGORY_OPTIONS[0];

class SearchBarComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      catOption: DEFAULT_CAT
    };
  }

  handleSelect(eventKey) {
    let newCatOption = CATEGORY_OPTIONS.filter( d => d.name === eventKey )[0];
    this.setState({ catOption: newCatOption });
  }

  handleSubmit(e) {
    e.preventDefault();
    let query = this.getQuery();
    let newCat = this.state.catOption.name;
    let newQp = { q: query };
    if (newCat !== 'all') newQp.category = newCat;
    this.props.dispatch(push({ pathname: '/search', query: newQp }));
  }

  getQuery() {
    let el = document.getElementsByClassName(INPUT_CLASS)[0];
    return el.value;
  }

  renderDropdown() {
    let _title = this.state.catOption.displayName;
    let nodes = CATEGORY_OPTIONS.map( d => {
      let labelNode = (d.name === DEFAULT_CAT.name) ? 'All' : <CategoryLabel category={d.name} />;
      return <MenuItem className={style.dropdownItem} eventKey={d.name} key={d.name}>{labelNode}</MenuItem>;
    });
    return (
      <DropdownButton className={style.dropdown} id='bg-nested-dropdown' onSelect={this.handleSelect.bind(this)} title={_title}>
        {nodes}
      </DropdownButton>
    );
  }

  render() {
    let query = this.props.queryParams.q || '';
    return (
      <div className={style.container}>
        <form onSubmit={this.handleSubmit.bind(this)} ref='form'>
          {this.renderDropdown()}
          <Typeahead
            className={style.typeahead}
            customClasses={{ input: INPUT_CLASS }}
            options={[]}
            value={query}
          />
          <a className={`btn btn-primary ${style.searchBtn}`} href='#' onClick={this.handleSubmit.bind(this)}><i className='fa fa-search' /></a>
        </form>
        
      </div>
    );
  }
}

SearchBarComponent.propTypes = {
  dispatch: React.PropTypes.func,
  queryParams: React.PropTypes.object,
  searchUrl: React.PropTypes.string
};

function mapStateToProps(state) {
  let location = state.routing.locationBeforeTransitions;
  let _queryParams = location ? location.query : {};
  return {
    queryParams: _queryParams
  };
}

export { SearchBarComponent as SearchBarComponent };
export default connect(mapStateToProps)(SearchBarComponent);
