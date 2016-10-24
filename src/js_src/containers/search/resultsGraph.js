/*eslint-disable react/no-set-state */
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { createMemoryHistory } from 'react-router';

import { selectGraphData, selectQueryParams } from '../../selectors/searchSelectors';
import fetchData from '../../lib/fetchData';
import { receiveGraphResponse, setError, setPending } from './searchActions';
import { SEARCH_API_ERROR_MESSAGE } from '../../constants';

const BASE_SEARCH_URL = '/api/graph_search';
const DEFAULT_WIDTH = 600;

class ResultsGraphComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      width: DEFAULT_WIDTH
    };
  }

  // fetch data at start
  componentDidMount() {
    this.calcWidth();
    this.fetchData();
  }

  // fetch data whenever URL changes within /search
  componentDidUpdate (prevProps) {
    if (prevProps.queryParams !== this.props.queryParams) {
      this.fetchData();
    }
  }

  calcWidth() {
    let newWidth = this.refs.container.getBoundingClientRect().width;
    this.setState({ width: newWidth });
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
    return (
      <div ref='container'>
        <canvas height={this.state.width} ref='canvas' width={this.state.width} />
      </div>
    );
  }
}

ResultsGraphComponent.propTypes = {
  data: React.PropTypes.object, // { nodes: [], edges: [] }
  dispatch: React.PropTypes.func,
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
