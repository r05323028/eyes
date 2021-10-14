import { useDispatch, useSelector } from "react-redux";
import { useMount } from "react-use";
import { Link } from "react-router-dom";

import { sagaActions } from "../sagas";
import { setCurrentEntity } from "../reducers/entities";

import Spinner from "../components/Spinner";

import NetworkChart from "../components/NetworkChart";

const MAX_ENTITIES = 10;

const columns = [
  {
    name: "Name",
  },
  {
    name: "Count",
  },
];

const createTableData = (data) => {
  return (
    <div className="overflow-x-auto">
      <table className="table w-full">
        <thead>
          <th></th>
          {columns.map((column, index) => (
            <th key={index}>{column.name}</th>
          ))}
        </thead>
        <tbody>
          {data?.map((row, index) => (
            <tr key={index} className="hover">
              <th>{index}</th>
              <td>{row.name}</td>
              <td>{row.count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const EntitiesMenu = (props) => {
  const { entities, handleOnEntitySelect, currentEntity } = props;
  return (
    <>
      <div className="form-control">
        <div className="flex space-x-2">
          <select
            className="select select-bordered"
            onChange={(e) => handleOnEntitySelect(e.target.value)}
          >
            {entities.map((ent) => (
              <option>{ent}</option>
            ))}
          </select>
          <Link to={`/entity/${currentEntity}`} className="btn btn-primary">
            Go
          </Link>
        </div>
      </div>
    </>
  );
};

const Entities = (props) => {
  const allStatsEntitySummaries = useSelector(
    (state) => state.entities.allStatsEntitySummaries
  );
  const loaded = useSelector((state) => state.entities.status.loaded);
  const requesting = useSelector((state) => state.entities.status.requesting);
  const nodes = useSelector((state) => state.entities.nodes);
  const edges = useSelector((state) => state.entities.edges);
  const currentEntity = useSelector((state) => state.entities.currentEntity);
  const dispatch = useDispatch();
  useMount(() => {
    dispatch(sagaActions.requestAllStatsEntitySummaries({ limit: 100 }));
  });
  const handleOnEntitySelect = (entity) => {
    dispatch(setCurrentEntity(entity));
  };
  return (
    <>
      <h1 className="font-bold text-4xl my-5">Entities</h1>
      <div className="grid grid-cols-2 my-5">
        <div className="card bordered">
          <div className="card-body">
            <div className="card-title">Search Entity</div>
            <EntitiesMenu
              entities={allStatsEntitySummaries.map((ent) => ent.name)}
              handleOnEntitySelect={handleOnEntitySelect}
              currentEntity={currentEntity}
            />
          </div>
        </div>
      </div>
      <div className="grid grid-cols-2 grid-flow-col h-128 gap-5">
        <div className="card bordered">
          <div className="card-body">
            <div className="card-title">Top Entities</div>
            {createTableData(allStatsEntitySummaries.slice(0, MAX_ENTITIES))}
          </div>
        </div>
        <div className="card bordered">
          <div className="card-body">
            <div className="card-title">Entity Relationship</div>
            {requesting === true || loaded === false ? (
              <Spinner />
            ) : (
              <NetworkChart nodes={nodes} edges={edges} />
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default Entities;
