import React, { Component } from 'react';

class Table extends Component {
  renderHeader() {
    return (
      <tr>
        <th>Symbol</th>
        <th>Source</th>
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
          <td>SGD</td>
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

export default Table;
