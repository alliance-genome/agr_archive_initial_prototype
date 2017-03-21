import React, { Component } from 'react';

// import mockViewer from './transcript-viewer-full.png';
import style from './style.css';

class TranscriptViewer extends Component {
  render() {
    let jbrowseUrl = 'http://bw.scottcain.net/jbrowse/?data=data%2FDanio%20rerio&loc=25%3A14926862..14955898&tracks=DNA%2CAll%20Genes&highlight=';

    // let visualizationUrl = 'http://dev.alliancegenome.org:8891/?url=';

    let finalUrl = 'http://dev.alliancegenome.org:8891/?url=http%3A%2F%2Fbw.scottcain.net%2Fjbrowse%2F%3Fdata%3Ddata%252FCaenorhabditis%2520elegans%26loc%3DIV%253A12893065..12894996%26tracks%3DAll%2520Genes%26highlight%3D%26screenshot%3Dp20o0r0n0u0b1m111s000000z1~0h2500i0q0d0&format=PNG&delay=16000&width=600&height=300&zoom=1&quality=0.7';
    // http://dev.alliancegenome.org:8891/?url=http%3A%2F%2Fbw.scottcain.net%2Fjbrowse%2F%3Fdata%3Ddata%252FCaenorhabditis%2520elegans%26loc%3DIV%253A12893065..12894996%26tracks%3DAll%2520Genes%26highlight%3D%26screenshot%3Dp20o0r0n0u0b1m111s000000z1~0h2500i0q0d0&format=PNG&delay=16000&width=600&height=300&zoom=1&quality=0.7

    // let finalUrl = visualizationUrl + jbrowseUrl ;

    return (
      <div className={style.jbrowse}>
        <a href={jbrowseUrl} rel="noopener noreferrer" target='_blank'>
          <img src={finalUrl} />
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
