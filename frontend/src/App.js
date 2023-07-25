import "./App.css";
import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [size, setSize] = useState(0);
  useEffect(() => {
    axios.get("http://localhost:8000/api/square_size").then((res) => {
      console.log(res);
      setSize(res.data);
    });
  });
  return <div className="App">{size}</div>;
}

export default App;
