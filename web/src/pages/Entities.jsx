import { useDispatch, useSelector } from "react-redux";
import { useMount } from "react-use";

import { sagaActions } from "../sagas";

import Spinner from "../components/Spinner";

import NetworkChart from "../components/NetworkChart";

const Entities = (props) => {
  const loaded = useSelector((state) => state.entities.status.loaded);
  const requesting = useSelector((state) => state.entities.status.requesting);
  const nodes = useSelector((state) => state.entities.nodes);
  const edges = useSelector((state) => state.entities.edges);
  const dispatch = useDispatch();
  useMount(() => {
    dispatch(sagaActions.requestAllStatsEntitySummaries({ limit: 100 }));
  });
  return (
    <>
      <h1 className="font-bold text-4xl my-5">Entities</h1>
      <div className="grid grid-cols-2 grid-flow-col h-128">
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
