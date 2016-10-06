import React, { Component } from 'react';

import style from './style.css';
import { makeFieldDisplayName } from '../../lib/searchHelpers';

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
    let keys = Object.keys(highlight);
    let nodes = keys.map( d => {
      return (
        <div className={style.resultContainer} key={`srh${d}`}>
          <dt>{makeFieldDisplayName(d)}:</dt>
          <dd dangerouslySetInnerHTML={{ __html: highlight[d] }} />
        </div>
      );
    });
    return (
      <dl className={style.detailList}>
        {nodes}
      </dl>
    );
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
