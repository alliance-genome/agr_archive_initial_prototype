import React, { Component } from 'react';
// import ReactDOM from 'react-dom';
import {Table, Column, Cell} from 'fixed-data-table-2';

class Disease extends Component {
  render() {
    return (

 <Table
    className='table'
    rowHeight={5}
    rowsCount={1}
    width={500}
    height={500}
    headerHeight={5}>

    <Column
      header={<Cell>Col 1</Cell>}
      cell={<Cell>Column 1 static content</Cell>}
      width={200}
    />

  </Table>
   
    );
  }
}

export default Disease;

 


