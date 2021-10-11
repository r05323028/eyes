import { useParams } from "react-router-dom";

const Entity = (props) => {
  const { entityName } = useParams();
  return (
    <>
      <h1 className="font-bold text-4xl my-5">{entityName}</h1>
      <div className="grid grid-cols-2 grid-flow-col gap-5 m-5">
        <div className="card bordered">
          <div className="card-body">
            <div className="card-title">123</div>
          </div>
        </div>
        <div className="card bordered">
          <div className="card-body">
            <div className="card-title">123</div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Entity;
