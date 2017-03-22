import React, { Component } from 'react';
import Helmet from 'react-helmet';

class Help extends Component {
  render() {
    return (
      <div>
        <Helmet
           title="Help Using Alliance of Genome Resources "
           meta={[
               {property: 'og:title', content: 'Help'},
           ]} />
        <h1>Help</h1>
      </div>
    );
  }
}

export default Help;
