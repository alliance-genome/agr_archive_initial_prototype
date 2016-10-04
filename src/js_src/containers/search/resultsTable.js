import React, { Component } from 'react';

class ResultsTable extends Component {
  renderHeader() {
    return (
      <tr>
        <th>Symbol</th>
        <th>Name</th>
        <th>Synonym</th>
        <th>Source</th>
        <th>Species</th>
        <th>Gene Type</th>
        <th>Genomic Coordinates</th>
        <th>Relative Coordinates</th>
      </tr>
    );
  }

  renderRows() {
    return this.props.entries.map( (d, i) => {
      return (
        <tr key={`tr${i}`}>
          <td>{d.symbol}</td>
          <td>{d.name}</td>
          <td>{d.synonyms}</td>
          <td><a href={d.sourceHref} target='_new'>{d.geneId}</a></td>
          <td><i>{d.species}</i></td>
          <td>{d.geneType}</td>
          <td>{`${d.genomicStartCoordinates}:${d.genomicStopCoordinates}`}</td>
          <td>{`chri${d.genomicStartCoordinates}:${d.genomicStopCoordinates}`}</td>
        </tr>
      );
    });
  }

  render() {
    return (
      <div>
        <table className='table'>
          <thead className='thead-default'>
            {this.renderHeader()}
          </thead>
          <tbody>
            {this.renderRows()}
          </tbody>
        </table>
      </div>
    );
  }
}

ResultsTable.propTypes = {
  entries: React.PropTypes.array
};

export default ResultsTable;
