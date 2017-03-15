import React, { Component } from 'react';
import FlybaseDataGrid from 'react-flybase-datagrid';
import faker from 'faker';
import './agr.css';

function getHeaders(){

  var columns = [
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
}

const data = generateList();

class DiseaseTable extends Component {
  render() {
    return (

       <FlybaseDataGrid columns={getHeaders()} data={data} showDownloadButton={false} showFilter={false} />

    );
  }
}

export default DiseaseTable;
