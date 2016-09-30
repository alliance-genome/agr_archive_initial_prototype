import React, { Component } from 'react';

class Table extends Component {
  renderHeader() {
    return (
      <tr>
        <th>Symbol</th>
        <th>Organism</th>
        <th>Source</th>
        <th>Genomic Coordinates</th>
        <th>Relative Coordinates</th>
        <th>Description</th>
      </tr>
    );
  }

  renderRows() {
    return this.props.entries.map( (d, i) => {
      return (
        <tr key={`tr${i}`}>
          <td>{d.symbol}</td>
          <td><i>{d.organism}</i></td>
          <td><a href='#'>{d.source}</a></td>
          <td>{`${d.genomicStartCoordinates}:${d.genomicStopCoordinates}`}</td>
          <td>{`chri${d.genomicStartCoordinates}:${d.genomicStopCoordinates}`}</td>
          <td>Lorem ipsum <mark>dolor</mark> sit amet, consectetur adipiscing elit, sed do eiusmod tempor</td>
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

Table.propTypes = {
  entries: React.PropTypes.array
};

export default Table;
