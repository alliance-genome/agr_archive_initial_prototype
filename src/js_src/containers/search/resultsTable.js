import React, { Component } from 'react';

import style from './style.css';
import DetailList from './detailList';

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
        <th>Match By</th>
      </tr>
    );
  }

  renderRows() {
    return this.props.entries.map( (d, i) => {
      return (
        <tr key={`tr${i}`}>
          <td dangerouslySetInnerHTML={{ __html: d.symbol }} />
          <td dangerouslySetInnerHTML={{ __html: d.name }} />
          <td dangerouslySetInnerHTML={{ __html: d.synonyms }} />
          <td><a dangerouslySetInnerHTML={{ __html: d.geneId }} href={d.sourceHref} target='_new' /></td>
          <td><i dangerouslySetInnerHTML={{ __html: d.species }} /></td>
          <td dangerouslySetInnerHTML={{ __html: d.geneType }} />
          <td>{`${d.genomicStartCoordinates}:${d.genomicStopCoordinates}`}</td>
          <td>{`chri${d.genomicStartCoordinates}:${d.genomicStopCoordinates}`}</td>
          <td>{this.renderHighlight(d.highlight)}</td>
        </tr>
      );
    });
  }

  renderHighlight(highlight) {
    let _data = highlight;
    let _fields = Object.keys(_data);
    return <DetailList data={_data} fields={_fields} />;
  }

  render() {
    return (
      <div className={style.tableContainer}>
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
