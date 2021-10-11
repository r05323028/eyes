import React from "react";
import Navbar from "./components/Navbar";
import Container from "./components/Container";

import Home from "./pages/Home";
import Articles from "./pages/Articles";
import Entities from "./pages/Entities";

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Entity from "./pages/Entity";

const navs = [
  {
    name: "Home",
    link: "/",
  },
  {
    name: "Articles",
    link: "/articles",
  },
  {
    name: "Entities",
    link: "/entities",
  },
];

function App() {
  return (
    <>
      <Router>
        <Navbar navs={navs} />
        <Container>
          <Switch>
            <Route path="/entity/:entityName">
              <Entity />
            </Route>
            <Route path="/entities">
              <Entities />
            </Route>
            <Route path="/articles">
              <Articles />
            </Route>
            <Route path="/">
              <Home />
            </Route>
          </Switch>
        </Container>
      </Router>
    </>
  );
}

export default App;
