const NON_HIGHLIGHTED_FIELDS = ['id', 'sourceHref', 'href', 'category'];
const JOIN_HIGHLIGHT_BY = '...';
const FILTER_ORDER = ['gene_type', 'species'];

import { makeFieldDisplayName } from '../lib/searchHelpers';

// takes the fields in responseObj.highlights and replaces the shallow values in responseObj
// also return highlight values as strings like '<em>val</em>...<em>val2</em>' instead of array
export function injectHighlightIntoResponse(responseObj) {
  let high = responseObj.highlights || {};
  let highKeys = Object.keys(high);
  let simpleHighObj = {};
  highKeys.forEach( key => {
    let highArr = high[key];
    let highStr = highArr.reduce( (prev, current, i) => {
      let suffix = (i === highArr.length - 1) ? '' : JOIN_HIGHLIGHT_BY;
      return prev + current + suffix;
    }, '');
    simpleHighObj[key] = highStr;
    // don't highlight some fields
    if (NON_HIGHLIGHTED_FIELDS.indexOf(key) < 0) {
      responseObj[key] = highStr;
    }
  });
  responseObj.highlights = simpleHighObj;
  return responseObj;
}

export function parseResults(results) {
  return results.map( d => { 
    switch (d.category) {
    case 'gene':
      return parseGeneResult(d);
    case 'go':
      return parseGoResult(d);
    case 'disease':
      return parseDiseaseResult(d);
    case 'ortholog group':
      return parseOrthoGroupResult(d);
    default:
      return parseDefaultResult(d);
    }
  });
}

export function parseAggs(rawAggs, queryObject) {
  // first sort them
  rawAggs = rawAggs.sort( (a, b) => (FILTER_ORDER.indexOf(a.key) < FILTER_ORDER.indexOf(b.key)) );
  return rawAggs.map( d => {
    let _values = d.values.map( _d => {
      let currentValue = queryObject[d.key];
      let _isActive;
      // look at array fields differently
      if (typeof currentValue === 'object') { 
        _isActive = (currentValue.indexOf(_d.key) >= 0);
      } else {
        _isActive = _d.key === currentValue;
      }
      return {
        name: _d.key,
        displayName: makeFieldDisplayName(_d.key),
        key: _d.key,
        total: _d.total,
        isActive: _isActive
      };
    });
    return {
      name: d.key,
      displayName: makeFieldDisplayName(d.key),
      key: d.key,
      values: _values
    };
  });
}

// search result individual entry parsers
function parseGeneResult(_d) {
  let d = injectHighlightIntoResponse(_d);
  return {
    symbol: d.gene_symbol || '(no symbol)',
    category: d.category || 'gene',
    display_name: d.gene_symbol,
    href: d.href,
    name: d.name,
    gene_id: d.id || '(no ID)',
    sourceHref: d.href,
    synonyms: d.gene_synonyms,
    gene_type: makeFieldDisplayName(d.gene_type),
    genomic_coordinates: d.genomic_coordinates,
    relative_coordinates: d.relative_coordinates,
    species: d.species,
    highlight: d.highlights
  };
}

function parseGoResult(_d) {
  let d = injectHighlightIntoResponse(_d);
  return {
    category: d.category,
    display_name: d.name,
    go_branch: makeFieldDisplayName(d.go_type),
    highlight: d.highlights,
    href: d.href,
    name: d.name,
    synonyms: d.go_synonyms
  };
}

function parseDiseaseResult(_d) {
  let d = injectHighlightIntoResponse(_d);
  return {
    associated_genes: d.associated_genes,
    category: d.category,
    display_name: d.name,
    go_branch: d.go_branch,
    highlight: d.highlights,
    href: d.href,
    name: d.name,
    omim_id: d.id,
    synonyms: d.synonym
  };
}

function parseOrthoGroupResult(d) {
  return parseDefaultResult(d);
}

function parseDefaultResult(_d) {
  let d = injectHighlightIntoResponse(_d);
  return {
    associated_genes: d.associated_genes,
    category: d.category || 'gene',
    display_name: d.name,
    highlight: d.highlights,
    href: d.href,
    name: d.name,
    synonyms: d.synonym
  };
}
