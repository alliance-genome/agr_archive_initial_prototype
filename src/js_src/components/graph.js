/*eslint-disable react/no-set-state */
import React, { Component } from 'react';
import getSpeciesColorScale from '../lib/getSpeciesColorScale';

const MAX_HEIGHT = 350;
const TARGET_ID = 'j-agr-sigma-target';

class Graph extends Component {
  // fetch data whenever URL changes within /search
  componentDidUpdate (prevProps) {
    if (prevProps.data !== this.props.data) {
      this.drawGraph();
    }
  }

  getHeight() {
    return MAX_HEIGHT;
  }

  getEdges() {
    let data = this.props.data;
    let rawEdges = data.edges;
    return rawEdges.map( (d, i) => {
      d.id = `e${i}`;
      d.color = '#e2e2e2';
      return d;
    });
  }

  getNodes() {
    let colorScale = getSpeciesColorScale();
    let length = this.props.data.nodes.length;
    return this.props.data.nodes.map( (d, i) => {
      d.color = colorScale(d.species);
      d.label = d.name;
      d.x = Math.cos(Math.PI * 2 * i / length);
      d.y = Math.sin(Math.PI * 2 * i / length);
      d.size = d.direct ? 1 : 0.75;
      return d;
    });
  }

  drawGraph() {
    let _nodes = this.getNodes();
    if (!_nodes.length) return;
    let _graph = {
      nodes: _nodes,
      edges: this.getEdges()
    };
    if (this.s) {
      this.s.graph.clear();
      this.s.refresh();
    }
    this.s = new sigma({
      graph: _graph,
      container: TARGET_ID,
      settings: {
        labelThreshold: 100,
        minNodeSize: 0,
        maxNodeSize: 3,
      }
    });
    this.s.startForceAtlas2();
  }

  render() {
    return (
      <div ref='container'>
        <div id={TARGET_ID} style={{ height: this.getHeight() }} />
      </div>
    );
  }
}

Graph.propTypes = {
  data: React.PropTypes.object // { nodes: [], edges: [] }
};

export default Graph;
