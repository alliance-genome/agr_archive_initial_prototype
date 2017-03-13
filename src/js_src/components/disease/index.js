import React, { Component } from 'react';
import FlybaseDataGrid from 'react-flybase-datagrid';
import faker from 'faker';
import './agr.css';
import {StyleSheet, css} from 'aphrodite';

const styles = StyleSheet.create({
 column: {
  backgroundColor: '#000',
 },
 field_label: {
  backgroundColor: '#000',
  borderColor: '#000000',
  borderRight: '1px',
  borderBottom: '1px',
  borderTop: '0px',
  fontWeight: 'bold',
  wordWrap: 'break-word',

  height: '100%',
  width: '100%',
 },
 wrapperStyles: {
    // marginTop: '1rem',
    // marginLeft: '1rem',
    // marginRight: '3rem',
    // border: 'none',
    // overflow:'hidden',
    // height: '100%',
    // borderBottom: "1px solid #000000"
  },
  newTableHeader: {
    // color: '#000',
    // fontSize: '12px',
    // lineHeight: '1',
    // background: '#FFFFFF',
    // border: 'none',

  },
  newCellBorder: {
    // borderBottomStyle: 'solid',
    // borderBottomWidth: '1px',
    // borderBottom: '1px solid #000000',
    backgroundColor: '#ffffff',
    border: '1px',
  }
});


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
};

const data = generateList();

class DiseaseTable extends Component {
  render() {
    return (

       <FlybaseDataGrid data={data} columns={getHeaders()} showDownloadButton={false} showFilter={false} style={styles} />

    );
  }
}

export default DiseaseTable;
