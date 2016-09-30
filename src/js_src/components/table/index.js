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
        <ul className='nav nav-tabs'>
          <li className='nav-item'>
            <a className='nav-link active'><i className='fa fa-table' /> Table</a>
          </li>
          <li className='nav-item'>
            <a className='nav-link'><i className='fa fa-th-list' /> List</a>
          </li>
        </ul>
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
