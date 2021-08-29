import React from "react";
import Navbar from "./components/Navbar";
import Container from "./components/Container";

import Home from "./pages/Home";

const navs = [
  {
    name: "Home",
    link: "/",
  },
];

function App() {
  return (
    <>
      <Navbar navs={navs} />
      <Container>
        <Home />
      </Container>
    </>
  );
}

export default App;
