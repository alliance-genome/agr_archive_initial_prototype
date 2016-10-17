/*eslint-disable react/no-set-state */
import React, { Component } from 'react';
import { connect } from 'react-redux';
import Autosuggest from 'react-autosuggest';
import { push } from 'react-router-redux';
import { DropdownButton, MenuItem } from 'react-bootstrap';

import style from './style.css';
import CategoryLabel from '../../search/categoryLabel';
import fetchData from '../../../lib/fetchData';
// import OptionsList from './optionsList';

const AUTO_BASE_URL = '/api/search_autocomplete';
const INPUT_CLASS = 'react-autosuggest__input';
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

  handleClear() {
    this.setState({ autoOptions: [] });
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

  handleFetchData() {
    let query = this.getQuery();
    let cat = this.state.catOption.name;
    let catSegment = cat === DEFAULT_CAT.name ? '' : ('&category=' + cat);
    let url = AUTO_BASE_URL + '?q=' + query + catSegment;
    fetchData(url)
      .then( (data) => {
        let newOptions = data.results || [];
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
    let _getSuggestionValue = ( d => d.name );
    let _inputProps = {
      placeholder: 'search a gene, GO term, or disease',
      value: query,
      onChange: this.handleFetchData.bind(this)
    };
    let _renderSuggestion = (d) => {
      return <div>{d.name}</div>;
    };
    return (
      <div className={style.container}>
        <form onSubmit={this.handleSubmit.bind(this)} ref='form'>
          {this.renderDropdown()}
          <Autosuggest
            getSuggestionValue={_getSuggestionValue}
            inputProps={_inputProps}
            onSuggestionsFetchRequested={this.handleFetchData}
            onSuggestionsClearRequested={this.handleClear}
            renderSuggestion={_renderSuggestion}
            suggestions={this.state.autoOptions}
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
