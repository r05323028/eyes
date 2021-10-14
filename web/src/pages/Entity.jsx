import _ from "lodash";
import moment from "moment";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { useMount } from "react-use";
import { sagaActions } from "../sagas";
import { ResponsiveLine } from "@nivo/line";
import Spinner from "../components/Spinner";
import NetworkChart from "../components/NetworkChart";

const createBoardChartData = (boardStats) => {
  return _(boardStats)
    .groupBy("board")
    .map((objs, key) => {
      return {
        id: key,
        data: _.sortBy(
          _.map(objs, (obj) => ({
            x: moment(obj.dt).format("YYYY-MM-DD"),
            y: obj.count,
          })),
          "x"
        ),
      };
    })
    .value();
};

const createLineChart = (lineData) => {
  return (
    <ResponsiveLine
      data={lineData}
      height={500}
      curve="basis"
      axisBottom={{
        format: "%b %d",
        tickValues: "every 2 days",
        legend: "date",
        legendPosition: "middle",
        legendOffset: 35,
      }}
      useMesh={false}
      enableGridX={false}
      enableGridY={false}
      colors={{ scheme: "nivo" }}
      xScale={{
        type: "time",
        format: "%Y-%m-%d",
        useUTC: false,
        precision: "day",
      }}
      xFormat="time:%Y-%m-%d"
      margin={{ top: 30, bottom: 75, left: 30, right: 125 }}
      enableSlices="x"
      legends={[
        {
          anchor: "bottom-right",
          direction: "column",
          justify: false,
          translateX: 100,
          translateY: 0,
          itemsSpacing: 0,
          itemDirection: "left-to-right",
          itemWidth: 80,
          itemHeight: 20,
          itemOpacity: 0.75,
          symbolSize: 12,
          symbolShape: "circle",
          symbolBorderColor: "rgba(0, 0, 0, .5)",
          effects: [
            {
              on: "hover",
              style: {
                itemBackground: "rgba(0, 0, 0, .03)",
                itemOpacity: 1,
              },
            },
          ],
        },
      ]}
    />
  );
};

const Entity = (props) => {
  const { entityName } = useParams();
  const dispatch = useDispatch();
  const edges = useSelector((state) => state.entity.edges);
  const nodes = useSelector((state) => state.entity.nodes);
  const boardStats = useSelector((state) => state.entity.boardStats);
  const linkStats = useSelector((state) => state.entity.linkStats);
  const requesting = useSelector((state) => state.entity.status.requesting);
  const posts = useSelector((state) => state.entity.posts);

  useMount(() => {
    dispatch(sagaActions.requestEntitySummary({ name: entityName }));
  });

  return (
    <>
      <h1 className="font-bold text-4xl my-5">Entity: {entityName}</h1>
      <div className="grid grid-cols-2 grid-flow-col gap-5 m-5">
        <div className="card bordered">
          <div className="card-body">
            <div className="card-title">Board Stats</div>
            {requesting ? (
              <Spinner />
            ) : (
              createLineChart(createBoardChartData(boardStats))
            )}
          </div>
        </div>
        <div className="card bordered">
          <div className="card-body">
            <div className="card-title">Entity Relationship</div>
            {requesting ? (
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

export default Entity;
