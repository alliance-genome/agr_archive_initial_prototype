/*eslint-disable react/no-set-state */
import React, { Component } from 'react';
import d3 from 'd3';

import getSpeciesColorScale from '../lib/getSpeciesColorScale';

class ChordDiagram extends Component {
  constructor(props) {
    super(props);
    this.state = {
      DOMSize: null
    };
  }

  componentDidMount() {
    this._calculateDOMSize();
  }

  componentDidUpdate() {
    this._renderSVG();
  }

  _calculateDOMSize () {
    let rect = this.refs.target.getBoundingClientRect();
    let size = Math.min(rect.width, rect.height);
    this.setState({ DOMSize: size });
  }

  _findNodeById(id) {
    for (let i = this.props.data.nodes.length - 1; i >= 0; i--) {
      let thisNode = this.props.data.nodes[i];
      if (thisNode.id === id) return thisNode;
    }
    return null;
  }

  // d3-fu like https://bl.ocks.org/mbostock/7607999
  _renderSVG () {
    let colorScale = getSpeciesColorScale();
    let size = this.state.DOMSize;
    if (!size) return;
    // create layout functions
    let diameter = size,
      radius = diameter / 2,
      innerRadius = radius - 75;
    let cluster = d3.layout.cluster()
      .size([360, innerRadius])
      .sort(null)
      .value(function(d) { return d.size; });
    let bundle = d3.layout.bundle();
    let line = d3.svg.line.radial()
      .interpolate('bundle')
      .tension(0.85)
      .radius(function(d) { return d.y; })
      .angle(function(d) { return d.x / 180 * Math.PI; });
    let sortedData = this.props.data.nodes.sort( (a, b) => {
      return d3.ascending(a.species, b.species);
    });
    // prepare data
    let nodesData = cluster.nodes({ name: '', children: sortedData });

    let links = this._packageEdges();
    // d3 DOM rendering
    let filteredNodesData = nodesData.filter(function(n) { return !n.children; });
    let nodeTarget = d3.select(this.refs.nodeTarget);
    let node = nodeTarget.selectAll('.c-node')
      .data(filteredNodesData, ( d => d.name ));
    node.exit().remove();
    node
      .enter().append('rect')
      .attr('class', 'c-node');
    node.transition()
      .attr({
        width: 4,
        height: 4,
        fill: ( d => colorScale(d.species)),
        transform: function(d) {
          return 'rotate(' + (d.x - 90) + ')translate(' + (d.y + 8) + ',0)' + (d.x < 180 ? '' : 'rotate(180)');
        }
      });
    let link = nodeTarget.selectAll('.link-node')
      .data(bundle(links));
    link.enter().append('path')
      .attr({
        'class': 'link-node',
        fill: 'none',
        stroke: '#e2e2e2',
        'stroke-dasharray': `${size} ${size}`,
        'stroke-dashoffset': size,
        d: line
      });
    link.exit().remove();
    link.transition().duration(1000)
      .attr({
        'stroke-dasharray': `${size} 0`,
        'stroke-dashoffset': 0,
        d: line
      });
  }

  _packageEdges() {
    return this.props.data.edges.map( (d) => {
      return { source: this._findNodeById(d.source), target: this._findNodeById(d.target) };
    });
  }

  render() {
    let svgSize = this.state.DOMSize || 100;
    let halfSize = svgSize / 2;
    return (
      <div ref='target' style={{ width: '100%', height: '100%' }}>
        <svg height={svgSize} ref='svg' width={svgSize} >
          <g  className='node-target' ref='nodeTarget' transform={`translate(${halfSize},${halfSize})`} />
        </svg>
      </div>
    );
  }
}

ChordDiagram.propTypes = {
  data: React.PropTypes.object // { nodes: [], edges: [] }
};

export default ChordDiagram;
