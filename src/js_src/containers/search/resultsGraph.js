import React, { Component } from 'react';
import { connect } from 'react-redux';
import { createMemoryHistory } from 'react-router';

import { selectGraphData, selectQueryParams } from '../../selectors/searchSelectors';
import fetchData from '../../lib/fetchData';
import { receiveGraphResponse, setError, setPending } from './searchActions';
import { SEARCH_API_ERROR_MESSAGE } from '../../constants';
import Graph from '../../components/graph';
import ChordDiagram from '../../components/chordDiagram';

const BASE_SEARCH_URL = '/api/graph_search';

class ResultsGraphComponent extends Component {
  // fetch data at start
  componentDidMount() {
    this.fetchData();
  }

  // fetch data whenever URL changes within /search
  componentDidUpdate (prevProps) {
    if (prevProps.queryParams !== this.props.queryParams) {
      this.fetchData();
    }
  }

  fetchData() {
    let tempHistory = createMemoryHistory('/');
    let graphSearchUrl = tempHistory.createPath({ pathname: BASE_SEARCH_URL, query: this.props.queryParams });
    this.props.dispatch(setPending(true));
    fetchData(graphSearchUrl)
      .then( (data) => {
        this.props.dispatch(receiveGraphResponse(data));
        this.props.dispatch(setError(false));
        this.props.dispatch(setPending(false));
      })
      .catch( (e) => {
        this.props.dispatch(setPending(false));
        if (process.env.NODE_ENV === 'production') {
          this.props.dispatch(setError(SEARCH_API_ERROR_MESSAGE));
        } else {
          throw(e);
        }
      });
  }

  render() {
    let vizNode = (this.props.mode === 'chord') ? <ChordDiagram data={this.props.data} /> : <Graph data={this.props.data} />;
    return (
      <div ref='container' style={{ width: '100%', height: 600 }}>
        {vizNode}
      </div>
    );
  }
}

ResultsGraphComponent.propTypes = {
  data: React.PropTypes.object, // { nodes: [], edges: [] }
  dispatch: React.PropTypes.func,
  mode: React.PropTypes.string,
  queryParams: React.PropTypes.object
};

function mapStateToProps(state) {
  return {
    data: selectGraphData(state),
    queryParams: selectQueryParams(state)
  };
}

export { ResultsGraphComponent as ResultsGraphComponent };
export default connect(mapStateToProps)(ResultsGraphComponent);
