import React, { Component } from 'react';
import Helmet from 'react-helmet';

class Home extends Component {
  render() {
    return (
      <div>
        <Helmet
           title="Home - Alliance of Genome Resources"
           meta={[
               {property: 'og:title', content: 'Home'},
           ]} />
        <h1>Home</h1>
      </div>
    );
  }
}

export default Home;
