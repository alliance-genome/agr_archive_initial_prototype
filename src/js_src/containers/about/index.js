import React, { Component } from 'react';
import Helmet from 'react-helmet';

class About extends Component {
  render() {
    return (
      <div>
        <Helmet
           title="About Us - Alliance of Genome Resources"
           meta={[
               {property: 'og:title', content: 'About'},
           ]} />
        <h1>About</h1>
      </div>
    );
  }
}

export default About;
