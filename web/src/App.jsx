import React from "react";
import Navbar from "./components/Navbar";
import Container from "./components/Container";

import Home from "./pages/Home";
import Articles from "./pages/Articles";

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

const navs = [
  {
    name: "Home",
    link: "/",
  },
  {
    name: "Articles",
    link: "/articles",
  },
];

function App() {
  return (
    <>
      <Router>
        <Navbar navs={navs} />
        <Container>
          <Switch>
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
