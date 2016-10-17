/*eslint-disable react/no-set-state */
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Typeahead } from 'react-typeahead';
import { push } from 'react-router-redux';
import { DropdownButton, MenuItem } from 'react-bootstrap';

import style from './style.css';
import CategoryLabel from '../../search/categoryLabel';
import fetchData from '../../../lib/fetchData';
import OptionsList from './optionsList';

const AUTO_BASE_URL = '/api/search_autocomplete';
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
      autoOptions: [],
      catOption: DEFAULT_CAT,
      isFocused: false
    };
  }

  dispatchSearchFromQuery(query) {
    let newCat = this.state.catOption.name;
    let newQp = { q: query };
    if (newCat !== 'all') newQp.category = newCat;
    this.props.dispatch(push({ pathname: '/search', query: newQp }));
  }

  handleBlur() {
    this.setState({ isFocused: false }) ;
  }

  handleFocus() {
    this.setState({ isFocused: true }) ;
  }

  handleOptionSelected(selected) {
    this.dispatchSearchFromQuery(selected);
  }

  handleSelect(eventKey) {
    let newCatOption = CATEGORY_OPTIONS.filter( d => d.name === eventKey )[0];
    this.setState({ catOption: newCatOption });
  }

  handleSubmit(e) {
    if (e) e.preventDefault();
    this.dispatchSearchFromQuery(this.getQuery());
  }

  handleKeyUp() {
    let query = this.getQuery();
    let cat = this.state.catOption.name;
    let catSegment = cat === DEFAULT_CAT.name ? '' : ('&category=' + cat);
    let url = AUTO_BASE_URL + '?q=' + query + catSegment;
    fetchData(url)
      .then( (data) => {
        let raw = data.results || [];
        let newOptions = raw.map( d => d.name );
        this.setState({ autoOptions: newOptions });
      });
  }

  getOptions() {
    return (this.state.isFocused) ? this.state.autoOptions : [];
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
            customListComponent={OptionsList}
            customClasses={{ input: INPUT_CLASS }}
            onBlur={this.handleBlur.bind(this)}
            onFocus={this.handleFocus.bind(this)}
            onOptionSelected={this.handleOptionSelected.bind(this)}
            filterOption={(d) => d}
            onKeyUp={this.handleKeyUp.bind(this)}
            options={this.getOptions()}
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
