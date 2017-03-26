import React, {Component} from 'react';

import style from './style.css';
// import axios from 'axios';
// import jquery from 'jquery';


class TranscriptViewer extends Component {

  constructor(props) {
    super(props);
    this.state = {imageStatus: 'loading'};
  }

  handleImageErrored() {
    this.setState({imageStatus: 'Error loading transcript preview.'});
  }

  handleImageLoaded() {
    this.setState({imageStatus: ''});
  }

  generateHash(inputString) {
    var hash = 0, i, chr;
    if (inputString.length === 0) return hash;
    for (i = 0; i < inputString.length; i++) {
      chr = inputString.charCodeAt(i);
      hash = ((hash << 5) - hash) + chr;
      hash |= 0; // Convert to 32bit integer
    }
    return hash;
  }


  render() {
    // let externalPrefix = 'http://bw.scottcain.net/jbrowse/?data=data%2F';
    let externalPrefix = 'http://34.208.22.23/jbrowse/overview.html?data=data%2F';
    let internalPrefix = 'http://localhost/jbrowse/overview.html?data=data%2F';
    // let visualizationUrl = 'http://dev.alliancegenome.org:8891/?url=';
    // let delay = 5000;
    // let pngSuffix = '&format=PNG&delay=' + delay + '&width=600&height=300&zoom=1&quality=0.7';
    // location based data
    // let locationString = this.props.fmin && this.props.fmax ? this.props.chromosome + ':' + this.props.fmin + '..' + this.props.fmax : this.props.geneSymbol;
    let fmin = this.props.fmin ? this.props.fmin : 10000;
    let fmax = this.props.fmax ? this.props.fmax : 20000;
    let locationString = this.props.chromosome + ':' + fmin + '..' + fmax;
    let uniqueLocation = encodeURI(this.props.species) + '&loc=' + encodeURI(locationString);

    let geneSymbolUrl = '&lookupSymbol='+this.props.geneSymbol;
    let internalJbrowseUrl = internalPrefix + uniqueLocation + '&tracks=All%20Genes&highlight='+ geneSymbolUrl;
    let externalJbrowseUrl = externalPrefix + uniqueLocation + '&tracks=All%20Genes&highlight='+geneSymbolUrl;

    // TODO: move EVERYTHING to the externalJBrowseUrl
    // let finalUrl = visualizationUrl + encodeURIComponent(externalJbrowseUrl.replace('DNA%2C', '')) + pngSuffix;
    // let finalUrl = visualizationUrl + encodeURIComponent(internalJbrowseUrl.replace('DNA%2C', '')) ;
    // let visualizationUrl = visualizationPrefix.replace('@IMAGEID@', 'snapshots/' + encodeURI(this.props.species) +'/' + encodeURI(locationString)+ '.jpeg') + uniqueLocation + '&tracks=All%20Genes&highlight=';
    //
    // let virualizationUrl2 = 'https://phantomjscloud.com/api/browser/v2/a-demo-key-with-low-quota-per-ip-address/?request={url:'+encodeURI('\"'+externalJbrowseUrl+'\"')+',renderType:"jpg"}';

    return (
      <div className={style.jbrowse}>
        {/*{alert(visualizationUrl)}*/}
        {/*<a href={externalJbrowseUrl}>*/}
        <a href={externalJbrowseUrl.replace('overview.html','index.html')}>Genome Viewer<i className="fa fa-link"></i> </a>
        <a href={externalJbrowseUrl}>Overview<i className="fa fa-link"></i> </a>
        <iframe id="genomeFrame" className={style.jbrowse} src={externalJbrowseUrl}/>
        {/*</a>*/}
        {/*<a href={externalJbrowseUrl} rel="noopener noreferrer" target='_blank'>*/}
          {/*<img*/}
            {/*onError={this.handleImageErrored.bind(this)}*/}
            {/*onLoad={this.handleImageLoaded.bind(this)}*/}
            {/*src={virualizationUrl2}*/}
          {/*/>*/}
        {/*</a>*/}
        {/*{this.state.imageStatus === 'loading'*/}
        {/*? <div>Loading ... <img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Loading_icon.gif"/></div>*/}
        {/*: ''*/}
        {/*}*/}
      </div>
    );
  }


}

TranscriptViewer.propTypes = {
  chromosome: React.PropTypes.string,
  fmax: React.PropTypes.number,
  fmin: React.PropTypes.number,
  geneSymbol: React.PropTypes.string.isRequired,
  species: React.PropTypes.string.isRequired,
};

export default TranscriptViewer;

