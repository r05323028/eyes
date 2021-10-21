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

const Timeline = (props) => {
  const { posts, requesting } = props;
  const createLeftCard = ({ title, content, dt }) => {
    return (
      <div class="mb-8 flex justify-between flex-row-reverse items-center w-full left-timeline">
        <div class="order-1 w-5/12"></div>
        <div class="z-20 flex items-center order-1 shadow-xl w-24 h-8">
          <h1 class="mx-auto text-primary font-semibold text-lg">
            {moment(dt).format("YYYY-MM-DD HH:MM")}
          </h1>
        </div>
        <div class="order-1 bg-neutral-content rounded-lg shadow-xl w-5/12 px-6 py-4">
          <h3 class="mb-3 font-bold text-white text-xl">{title}</h3>
          <p class="text-sm font-medium leading-snug tracking-wide text-white text-opacity-100">
            {content.slice(0, 100) + "..."}
          </p>
        </div>
      </div>
    );
  };
  const createRightCard = ({ title, content, dt }) => {
    return (
      <div class="mb-8 flex justify-between items-center w-full right-timeline">
        <div class="order-1 w-5/12"></div>
        <div class="z-20 flex items-center order-1 shadow-xl w-24 h-8">
          <h1 class="mx-auto font-semibold text-lg text-white">
            {moment(dt).format("YYYY-MM-DD HH:MM")}
          </h1>
        </div>
        <div class="order-1 bg-primary rounded-lg shadow-xl w-5/12 px-6 py-4">
          <h3 class="mb-3 font-bold text-base-300 text-xl">{title}</h3>
          <p class="text-sm leading-snug tracking-wide text-base-300 text-opacity-100">
            {content.slice(0, 100) + "..."}
          </p>
        </div>
      </div>
    );
  };
  return (
    <div class="container mx-auto w-full h-full">
      <div class="relative wrap overflow-hidden p-10 h-full">
        <div
          style={{ left: "50%" }}
          class="border-2-2 absolute border-opacity-20 border-gray-700 h-full border"
        ></div>
        {requesting ? (
          <Spinner />
        ) : (
          posts.map((post, index) => {
            return (
              <>
                {index % 2 === 0
                  ? createLeftCard({
                      title: post.title,
                      content: post.content,
                      dt: post.createdAt,
                    })
                  : createRightCard({
                      title: post.title,
                      content: post.content,
                      dt: post.createdAt,
                    })}
              </>
            );
          })
        )}
      </div>
    </div>
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
  const requestingPosts = useSelector(
    (state) => state.entity.status.requestingPosts
  );

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
      <div className="grid grid-cols-1 grid-flow-col gap-5 m-5">
        <div className="card bordered">
          <div className="card-body">
            <div className="card-title">Timeline</div>
            <Timeline posts={posts} requesting={requestingPosts} />
          </div>
        </div>
      </div>
    </>
  );
};

export default Entity;
