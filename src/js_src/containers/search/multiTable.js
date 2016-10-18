/*eslint-disable react/sort-prop-types */
import React, { Component } from 'react';
import { connect } from 'react-redux';

import ResultsTable from './resultsTable';
import CategoryLabel from './categoryLabel';

import {
  selectQueryParams,
  selectGeneResults,
  selectGoResults,
  selectDiseaseResults,
  selectOrthoGroupResults,
  selectGeneTotal,
  selectGoTotal,
  selectDiseaseTotal,
  selectOrthoGroupTotal,
} from '../../selectors/searchSelectors';

class MultiTableComponent extends Component {
  renderGenes() {
    return (
      <div>
        <p>{this.props.geneTotal.toLocaleString()} <CategoryLabel category='gene' /></p>
        <ResultsTable category='gene' entries={this.props.geneResults} />
      </div>
    );
  }

  renderGo() {
    return (
      <div>
        <p>{this.props.goTotal.toLocaleString()} <CategoryLabel category='go' /></p>
        <ResultsTable category='go' entries={this.props.goResults} />
      </div>
    );
  }

  renderDisease() {
    return (
      <div>
        <p>{this.props.diseaseTotal.toLocaleString()} <CategoryLabel category='disease' /></p>
        <ResultsTable category='go' entries={this.props.diseaseResults} />
      </div>
    );
  }

  renderOrthoGroup() {
    return (
      <div>
        <p>{this.props.orthoGroupTotal.toLocaleString()} <CategoryLabel category='ortholog group' /></p>
        <ResultsTable category='go' entries={this.props.orthoGroupResults} />
      </div>
    );
  }

  render() {
    return (
      <div>
        {this.renderGenes()}
        {this.renderGo()}
        {this.renderDisease()}
        {this.renderOrthoGroup()}
      </div>
    );
  }
}

MultiTableComponent.propTypes = {
  queryParams: React.PropTypes.object,
  geneResults: React.PropTypes.array,
  goResults: React.PropTypes.array,
  diseaseResults: React.PropTypes.array,
  orthoGroupResults: React.PropTypes.array,
  geneTotal: React.PropTypes.number,
  goTotal: React.PropTypes.number,
  diseaseTotal: React.PropTypes.number,
  orthoGroupTotal: React.PropTypes.number
};

function mapStateToProps(state) {
  return {
    queryParams: selectQueryParams(state),
    geneResults: selectGeneResults(state),
    goResults: selectGoResults(state),
    diseaseResults: selectDiseaseResults(state),
    orthoGroupResults: selectOrthoGroupResults(state),
    geneTotal: selectGeneTotal(state),
    goTotal: selectGoTotal(state),
    diseaseTotal: selectDiseaseTotal(state),
    orthoGroupTotal: selectOrthoGroupTotal(state),
  };
}

export { MultiTableComponent as MultiTableComponent };
export default connect(mapStateToProps)(MultiTableComponent);
