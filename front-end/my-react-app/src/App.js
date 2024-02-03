

import React, { useEffect, useState } from 'react'
import Menu from './Components/menu/Menu'

function App() {
  const [data, setData] = useState([]);

  //useEffect(() => {
  //   async function fetchData() {
  //     var headers = {}
  //     const response = await fetch('http://127.0.0.1:5000/api/projects',{
  //       method : "GET",
  //       mode: 'cors',
  //       headers: headers
  //   }); // Endpoint a ser definido no 
  //     console.log(response)
  //     const result = await response.json();
  //     setData(result);
  //     console.log(result)
  //   }

  //   fetchData();
  // }, []);

  return (
    <div className="App">
       <Menu/>
    </div>
  );
}

export default App;
