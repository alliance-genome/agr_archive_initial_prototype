import React, { Component } from 'react';

import style from './style.css';

class ResultsList extends Component {
  renderRows() {
    return this.props.entries.map( (d, i) => {
      return (
        <div className={style.resultContainer} key={`sr${i}`} >
          <h3>
            <a href='#'>{d.symbol}</a>
          </h3>
          <dl>
            <dt>Name:</dt>
            <dd>{d.name}</dd>
            <dt>Synonym:</dt>
            <dd>{d.synonyms}</dd>
            <dt>Source:</dt>
            <dd><a href={d.sourceHref} target='_new'>{d.geneId}</a></dd>
            <dt>Species:</dt>
            <dd><i>{d.species}</i></dd>
            <dt>Gene Type:</dt>
            <dd>{d.geneType}</dd>
            <dt>Genomic Coordinates:</dt>
            <dd>{`${d.genomicStartCoordinates}:${d.genomicStopCoordinates}`}</dd>
            <dt>Relative Coordinates:</dt>
            <dd>{`chri${d.genomicStartCoordinates}:${d.genomicStopCoordinates}`}</dd>
            <dt>Description:</dt>
            <dd>Lorem ipsum <mark>dolor</mark> sit amet, consectetur adipiscing elit, sed do eiusmod tempor</dd>
          </dl>
          <hr />
        </div>
      );
    });
  }

  render() {
    return (
      <div>
        {this.renderRows()}
      </div>
    );
  }
}

ResultsList.propTypes = {
  entries: React.PropTypes.array
};

export default ResultsList;
