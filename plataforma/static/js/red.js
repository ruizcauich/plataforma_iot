// create an array with nodes
var nodes = new vis.DataSet([
    {id: 1, label: 'Node 1'},
    {id: 2, label: 'Node 2'},
    {id: 3, label: 'Node 3'},
    {id: 4, label: 'Node 4'},
    {id: 5, label: 'Node 5'},
  ]);
  
  // Create an array with edges
  var edges = new vis.DataSet([
    {from: 1, to: 3},
    {from: 1, to: 2},
    {from: 2, to: 4},
    {from: 2, to: 5},
  ]);
  
  //Create a network
  var container = document.getElementById('mynetwork')
  
  //provide the data in the vis format
  var data = {
    nodes: nodes,
    edges: edges
  };
  
  var options = {};
  
  //Initialize your network!
  var network =  new vis.Network(container,data,options)
  