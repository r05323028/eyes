import moment from "moment";
import { useSelector, useDispatch } from "react-redux";
import { useMount } from "react-use";
import { useRouteMatch } from "react-router";
import { Link } from "react-router-dom";

import { setCurrentTab } from "../reducers/article";
import { sagaActions } from "../sagas";

import Spinner from "../components/Spinner";
import LineChart from "../components/LineChart";

const fakeData = [
  {
    id: "japan",
    color: "hsl(37, 70%, 50%)",
    data: [
      {
        x: "plane",
        y: 151,
      },
      {
        x: "helicopter",
        y: 211,
      },
      {
        x: "boat",
        y: 137,
      },
      {
        x: "train",
        y: 165,
      },
      {
        x: "subway",
        y: 87,
      },
      {
        x: "bus",
        y: 145,
      },
      {
        x: "car",
        y: 58,
      },
      {
        x: "moto",
        y: 168,
      },
      {
        x: "bicycle",
        y: 69,
      },
      {
        x: "horse",
        y: 248,
      },
      {
        x: "skateboard",
        y: 216,
      },
      {
        x: "others",
        y: 82,
      },
    ],
  },
];

const createLineChart = (data) => {
  return <LineChart data={data} />;
};

const createStats = (numPosts, numComments) => {
  return (
    <div className="shadow stats">
      <div className="stat">
        <div className="stat-title">Monthly Posts</div>
        <div className="stat-value">{numPosts}</div>
        <div className="stat-desc">{moment().format("MMM YYYY")}</div>
      </div>
      <div className="stat">
        <div className="stat-title">Monthly Comments</div>
        <div className="stat-value">{numComments}</div>
        <div className="stat-desc">{moment().format("MMM YYYY")}</div>
      </div>
    </div>
  );
};

const createTable = (data, columns) => {
  return (
    <div className="overflow-x-auto">
      <table className="table w-full">
        <thead>
          <tr>
            <th></th>
            {columns.map((column, index) => (
              <th key={index}>{column.name}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data?.map((row, index) => (
            <tr key={index} className="hover">
              <th>{index}</th>
              <td>{row.board}</td>
              <td>{row.title}</td>
              <td>{row.author}</td>
              <td>{row.numComments}</td>
              <td>{moment(row.createdAt).format("YYYY-MM-DD hh:mm")}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const createTab = (tab, active, onClick, key) => {
  return (
    <Link key={key} to={tab.path} onClick={() => onClick(tab)}>
      <div className={`tab tab-lifted tab-lg ${active ? "tab-active" : ""}`}>
        {tab.name}
      </div>
    </Link>
  );
};

const Articles = (props) => {
  const { url } = useRouteMatch();
  const dispatch = useDispatch();
  const currentTab = useSelector((state) => state.article.currentTab);
  const articles = useSelector((state) => state.article.articles);
  const articleLoading = useSelector(
    (state) => state.article.status.requesting
  );
  const tabs = [
    {
      name: "PTT",
      path: `${url}/ptt`,
    },
    // {
    //   name: "Dcard",
    //   path: `${url}/dcard`,
    // },
  ];
  const columns = [
    {
      name: "Board",
    },
    {
      name: "Title",
    },
    {
      name: "Author",
    },
    {
      name: "# of Comments",
    },
    {
      name: "Created At",
    },
  ];

  useMount(() => {
    dispatch(sagaActions.requestPTTArticles());
  });

  const handleOnTabClick = (tab) => {
    dispatch(setCurrentTab(tab.name));
    switch (tab.name) {
      case "PTT":
        dispatch(sagaActions.requestPTTArticles());
        break;
      default:
        break;
    }
  };

  return (
    <>
      <h1 className="font-bold text-4xl my-5">Articles</h1>
      <div className="tabs">
        {tabs.map((tab, index) =>
          createTab(tab, currentTab === tab.name, handleOnTabClick, index)
        )}
      </div>
      <div className="grid grid-cols-2 grid-flow-col gap-5 m-5">
        <div className="card bordered">
          <div className="card-body">
            <div className="card-title">PTT</div>
            <p>Most visited forum in Taiwan.</p>
            <div className="card-actions">
              <button className="btn btn-primary">Go</button>
            </div>
          </div>
        </div>
        <div className="card bordered p-5">{createStats(426, 9487)}</div>
        <div className="card bordered p-5 row-span-2">
          {createLineChart(fakeData)}
        </div>
      </div>
      <div className="grid grid-cols-2 grid-flow-col"></div>
      <div className="card bordered m-5">
        <div className="card-body">
          <h2 className="card-title text-2xl">Latest Posts</h2>
          {articleLoading ? <Spinner /> : createTable(articles, columns)}
        </div>
      </div>
    </>
  );
};

export default Articles;
