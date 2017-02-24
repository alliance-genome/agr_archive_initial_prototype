import React, { Component } from 'react';

import mockViewer from './transcript-viewer-full.png';
import style from './style.css';

class TranscriptViewer extends Component {
  render() {
    let jbrowseUrl = 'http://bw.scottcain.net/jbrowse/';
    let tracks = 'All Genes';
    jbrowseUrl += '?data=' + encodeURIComponent('data/' + this.props.species);
    jbrowseUrl += '&loc=' + encodeURIComponent(this.props.geneSymbol);
    jbrowseUrl += '&tracks=' + encodeURIComponent(tracks);
    jbrowseUrl += '&nav=1&overview=1&tracklist=1&highlight=';

    return (
      <div className={style.jbrowse}>
        <a href={jbrowseUrl} rel="noopener noreferrer" target='_blank'>
          <img src={mockViewer} />
        </a>
      </div>
    );
  }
}

TranscriptViewer.propTypes = {
  geneSymbol: React.PropTypes.string.isRequired,
  species: React.PropTypes.string.isRequired,
};

export default TranscriptViewer;
