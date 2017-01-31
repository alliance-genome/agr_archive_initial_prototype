import React, {Component} from 'react';

class GenePage extends Component {
  render() {
    return (
      <div className='container'>
        // TODO: replace this placeholder content
        <h1>Gene {this.props.params.geneId}</h1>
      </div>
    );
  }
}

export default GenePage;
