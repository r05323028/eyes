import PropTypes from "prop-types";

import { Link } from "react-router-dom";

const createNav = ({ name, link }, index) => {
  return (
    <Link key={index} className="btn btn-ghost btn-sm rounded-btn" to={link}>
      {name}
    </Link>
  );
};

const Navbar = (props) => {
  return (
    <div className="navbar mb-2 shadow-lg bg-neutral text-neutral-content rounded-box">
      <div className="flex-none px-2 mx-2">
        <span className="text-xl font-bold">Eyes</span>
      </div>
      <div className="flex-1 px-2 mx-2">
        <div className="items-stretch hidden lg:flex">
          {props.navs.map(createNav)}
        </div>
      </div>
    </div>
  );
};

Navbar.propTypes = {
  navs: PropTypes.array.isRequired,
};

export default Navbar;
