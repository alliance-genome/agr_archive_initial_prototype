/*eslint-disable react/no-set-state */
import React, { Component } from 'react';
import d3 from 'd3';

import getSpeciesColorScale from '../lib/getSpeciesColorScale';

const BAND_SIZE = 14;

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

  getChromData() {
    if (!this.props.data) return null;
    let data = this.props.data.meta;
    if (!data) return [];
    return data.map( d => {
      return { name: d.name, length: d3.sum(d.chromosomes) };
    });
  }

  _renderSVG () {
    let colorScale = getSpeciesColorScale();
    let size = 300;//this.state.DOMSize;
    if (!size) return;
    let cData = this.getChromData();
    // create layout functions
    let diameter = size,
      radius = diameter / 2;
    const arc = d3.svg.arc()
      .outerRadius(radius)
      .innerRadius(radius - BAND_SIZE);
    const pie = d3.layout.pie()
      .sort(null)
      .value( d => d.length );
    let svg = d3.select(this.refs.svg);
    let chromArc = svg.selectAll('.chromArc')
      .data(pie(cData));
    chromArc.enter().append('path')
      .attr({
        class: 'chromArc',
      });
    chromArc.exit().remove();
    chromArc.attr({
      d: arc,
      fill: ( d => colorScale(d.data.name) )
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
