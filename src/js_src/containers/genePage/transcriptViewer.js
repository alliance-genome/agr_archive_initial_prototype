import React, {Component} from 'react';

// import mockViewer from './transcript-viewer-full.png';
import style from './style.css';

class TranscriptViewer extends Component {
  render() {
    let jbrowsePrefx = 'http://bw.scottcain.net/jbrowse/?data=data%2F';
    // location based data
    // var jbrowseUrl = jbrowsePrefx + encodeURI(this.props.species) + '&loc='+encodeURI(this.props.chromosome)+'%3A'+this.props.fmin +'..'+this.props.fmax+'&tracks=DNA%2CAll%20Genes&highlight=';
    let jbrowseUrl = jbrowsePrefx + encodeURI(this.props.species) + '&loc=' + encodeURI(this.props.geneSymbol) + '&tracks=DNA%2CAll%20Genes&highlight=';
    let visualizationUrl = 'http://dev.alliancegenome.org:8891/?url=';

    // original URL
    // let finalUrl = 'http://dev.alliancegenome.org:8891/?url=http%3A%2F%2Fbw.scottcain.net%2Fjbrowse%2F%3Fdata%3Ddata%252FCaenorhabditis%2520elegans%26loc%3DIV%253A12893065..12894996%26tracks%3DAll%2520Genes%26highlight%3D%26screenshot%3Dp20o0r0n0u0b1m111s000000z1~0h2500i0q0d0&format=PNG&delay=16000&width=600&height=300&zoom=1&quality=0.7';

    let delay = 5000;
    let pngSuffix = '&format=PNG&delay='+delay+'&width=600&height=300&zoom=1&quality=0.7';
    let hideControlsSuffix = '&tracklist=0&nav=0&tracklabels=0';

    let finalUrl = visualizationUrl + encodeURIComponent(jbrowseUrl.replace('DNA%2C', '') + hideControlsSuffix) + pngSuffix;
    return (
      <div className={style.jbrowse}>
        <a href={jbrowseUrl} rel="noopener noreferrer" target='_blank'>
          <img src={finalUrl}/>
        </a>
      </div>
    );
  }
}

TranscriptViewer.propTypes = {
  geneSymbol: React.PropTypes.string.isRequired,
  species: React.PropTypes.string.isRequired,
  fmin: React.PropTypes.number.isRequired,
  fmax: React.PropTypes.number.isRequired,
  chromosome: React.PropTypes.string.isRequired,
};

export default TranscriptViewer;
