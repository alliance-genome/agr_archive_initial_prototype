import React from 'react';
import {render} from 'react-dom';
import Component from 'react-flybase-datagrid';
import faker from 'faker';
import './dist/fixed-data-table.css';

// Table data as a list of array.

function getHeaders(){

 var columns =  [
   {id:'id', name:'ID'},
   {id:'name', name:'Name'},
   {id:'address', name:'Street Address'},
   {id:'state', name:'State'},
   {id:'zip', name:'Zip Code'}
 ];

 return columns;

}

function generateList(){
  var items = [];

  for (var i=1; i<=5000; i++){
   items.push({ id: i, name: faker.name.findName(), address: faker.address.streetAddress(), state: faker.address.stateAbbr(), zip: faker.address.zipCode()});
 }

 return items;
};

const data = generateList();

class Disease extends Component {
  render() {
    return (

    <div>
      <h1>datagrid1</h1>
      <Component data={data} columns={getHeaders()} showFilter={true} />
    </div>

    );
  }
}

export default Disease;
