import React from "react";
import ReactDOM from "react-dom/client";
// import App from "./App";
import Header from "./components/Header";
import Todos from "./components/Todos";
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <Header />
    <Todos />
  </React.StrictMode>
);
