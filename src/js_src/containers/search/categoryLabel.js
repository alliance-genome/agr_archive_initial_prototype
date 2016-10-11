import React, { Component } from 'react';

class CategoryLabel extends Component {
  render() {
    return <span>{this.props.category}</span>;
  }
}

CategoryLabel.propTypes = {
  category: React.PropTypes.string
};

export default CategoryLabel;
