import React, { Component } from 'react';

// import MethodHeader from './methodHeader';
// import MethodCell from './methodCell';
// import BooleanCell from './booleanCell';

// const columnNames = ['Species', 'Gene symbol', 'Score',
//   'Best score', 'Best reverse score', 'Method', 'Align'];

class DiseaseTable extends Component {

  render() {
    return(
     <div><h1>foo</h1></div>
    );
  }
}

DiseaseTable.propTypes = {
  data: React.PropTypes.arrayOf(
    React.PropTypes.shape({
      species: React.PropTypes.string,
      geneSymbol: React.PropTypes.string,
      geneURL: React.PropTypes.string,
      ncbiID: React.PropTypes.string,
      scoreNumerator: React.PropTypes.number,
      scoreDemominator: React.PropTypes.number,
      isBestScore: React.PropTypes.bool,
      isBestScoreReverse: React.PropTypes.bool,
      alignURL: React.PropTypes.string,
    })
  )
};

export default DiseaseTable;
