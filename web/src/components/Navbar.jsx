import PropTypes from "prop-types";

const createNav = ({ name, link }) => {
  return (
    <a class="btn btn-ghost btn-sm rounded-btn" href={link}>
      {name}
    </a>
  );
};

const Navbar = (props) => {
  return (
    <div className="navbar mb-2 shadow-lg bg-neutral text-neutral-content rounded-box">
      <div className="flex-none px-2 mx-2">
        <span className="text-lg font-bold">Eyes</span>
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
  nav: PropTypes.array.isRequired,
};

export default Navbar;
