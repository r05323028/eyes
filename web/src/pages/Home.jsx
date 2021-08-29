import PropTypes from "prop-types";

const Home = (props) => {
  return (
    <div className="hero min-h-screen bg-base-200">
      <div className="text-center hero-content">
        <div className="max-w-md">
          <h1 className="mb-5 text-5xl font-bold">{props.title}</h1>
          <p className="mb-5">{props.subtitle}</p>
        </div>
      </div>
    </div>
  );
};

Home.defaultProps = {
  title: "Eyes",
  subtitle: "Public Opinion Mining System focusing on Taiwanese forums",
};

Home.propTypes = {
  title: PropTypes.string,
  subtitle: PropTypes.string,
};

export default Home;
