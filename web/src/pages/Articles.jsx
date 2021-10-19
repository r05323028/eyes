import moment from "moment";
import { ResponsiveLine } from "@nivo/line";

import { useSelector, useDispatch } from "react-redux";
import { useMount, useKey } from "react-use";
import { useRouteMatch } from "react-router";
import { Link } from "react-router-dom";

import { setCurrentTab } from "../reducers/article";
import { sagaActions } from "../sagas";
import { setModalOpen } from "../reducers/article";

import Spinner from "../components/Spinner";

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

const createLineChart = (data) => {
  const lineData = [
    {
      id: "PTT",
      color: "hsl(37, 70%, 50%)",
      data: data?.map((row) => ({
        x: `${row.year}-${row.month}-${row.day}`,
        y: row.totalPosts,
      })),
    },
  ];
  return (
    <ResponsiveLine
      curve="basis"
      data={lineData}
      enableArea={true}
      axisBottom={{
        tickRotation: -45,
        legend: "date",
        legendPosition: "middle",
        orient: "bottom",
        legendOffset: 65,
      }}
      margin={{ top: 30, right: 30, bottom: 75, left: 65 }}
      useMesh={false}
      colors={{ scheme: "nivo" }}
      enablePoints={false}
      enableGridX={false}
      enableGridY={false}
    />
  );
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

const createTable = (data, columns, handleOnPostClick) => {
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
            <tr
              key={index}
              className="hover"
              onClick={() => handleOnPostClick(row)}
            >
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

const PostModal = (props) => {
  const { modalOpen, onClose, post, requesting } = props;

  return (
    <div
      id="article-modal"
      className={`modal ${modalOpen ? "modal-open" : ""}`}
    >
      <div className="modal-box h-2/3 overflow-y-scroll">
        {requesting ? (
          <div className="flex justify-center">
            <Spinner />
          </div>
        ) : (
          <>
            <h2 className="font-bold text-2xl my-5">{post.title}</h2>
            <div className="divider" />
            <p className="my-5">{post.content}</p>
            <div className="divider" />
            <div className="flex flex-col">
              {post.comments?.map((com) => (
                <div className="flex space-x-5">
                  <div>{com.reaction}</div>
                  <div>{com.author}: </div>
                  <div>{com.content}</div>
                </div>
              ))}
            </div>
            <div className="modal-action">
              <button className="btn" onClick={onClose}>
                Close
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

const Articles = (props) => {
  const { url } = useRouteMatch();
  const dispatch = useDispatch();
  const currentTab = useSelector((state) => state.article.currentTab);
  const requestingPost = useSelector(
    (state) => state.article.status.requestingPost
  );
  const currentPost = useSelector((state) => state.article.currentPost);
  const articles = useSelector((state) => state.article.articles);
  const pageInfo = useSelector((state) => state.article.pageInfo);
  const currentPage = useSelector((state) => state.article.currentPage);
  const modalOpen = useSelector((state) => state.article.status.modalOpen);
  const monthlySummary = useSelector((state) => state.article.monthlySummary);
  const dailySummaries = useSelector((state) => state.article.dailySummaries);
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

  useMount(() => {
    const now = new Date();
    dispatch(sagaActions.requestPTTArticles(pageInfo));
    dispatch(
      sagaActions.requestPTTMonthlySummary({
        source: 1,
        year: now.getFullYear(),
        month: now.getMonth() + 1,
      })
    );
    dispatch(
      sagaActions.requestPTTDailySummaries({
        source: 1,
        limit: 30,
      })
    );
  });
  useKey("Escape", () => {
    dispatch(setModalOpen(false));
  });

  const handleOnTabClick = (tab) => {
    const now = new Date();
    dispatch(setCurrentTab(tab.name));
    switch (tab.name) {
      case "PTT":
        dispatch(sagaActions.requestPTTArticles(pageInfo));
        dispatch(
          sagaActions.requestPTTMonthlySummary({
            source: 1,
            year: now.getFullYear(),
            month: now.getMonth() + 1,
          })
        );
        dispatch(
          sagaActions.requestPTTDailySummaries({
            source: 1,
            limit: 30,
          })
        );
        break;
      default:
        break;
    }
  };

  const handleOnPreviousClick = (e) => {
    e.preventDefault();
    dispatch(sagaActions.requestPTTArticlesPreviousPage(pageInfo));
  };
  const handleOnNextClick = (e) => {
    e.preventDefault();
    dispatch(sagaActions.requestPTTArticlesNextPage(pageInfo));
  };
  const handleOnPostClick = (post) => {
    dispatch(sagaActions.requestPost({ postId: post.postId }));
    dispatch(setModalOpen(true));
  };
  const handleOnPostClose = () => {
    dispatch(setModalOpen(false));
  };
  return (
    <>
      <PostModal
        onClose={handleOnPostClose}
        post={currentPost}
        modalOpen={modalOpen}
        requesting={requestingPost}
      />
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
              <a
                className="btn btn-primary"
                href="https://www.ptt.cc/bbs/hotboards.html"
                target="_blank"
                rel="noreferrer"
              >
                Go
              </a>
            </div>
          </div>
        </div>
        <div className="card bordered">
          <div className="card-body">
            {createStats(
              monthlySummary.totalPosts,
              monthlySummary.totalComments
            )}
          </div>
        </div>
        <div className="card bordered row-span-2">
          <div className="card-body">
            <div className="card-title">Trending</div>
            {createLineChart(dailySummaries)}
          </div>
        </div>
      </div>
      <div className="grid grid-cols-2 grid-flow-col"></div>
      <div className="card bordered m-5">
        <div className="card-body">
          <h2 className="card-title text-2xl">Latest Posts</h2>
          {articleLoading ? (
            <Spinner />
          ) : (
            createTable(articles, columns, handleOnPostClick)
          )}
          <div className="card-actions">
            <div className="btn-group">
              <button
                className={`btn ${currentPage > 1 ? "" : "btn-disabled"}`}
                onClick={handleOnPreviousClick}
              >
                Previous
              </button>
              <button
                type="button"
                className={`btn ${pageInfo.endCursor ? "" : "btn-disabled"}`}
                onClick={handleOnNextClick}
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Articles;
