import _ from "lodash";
import Gradient from "javascript-color-gradient";
import { createSlice } from "@reduxjs/toolkit";

const colorGradient = new Gradient();
colorGradient.setGradient("#2D8BD7", "#D70650");
colorGradient.setMidpoint(50);

const createNetworkNodes = (name, count, linkStats) => {
  let nodes = [];
  nodes.push({
    id: name,
    label: name,
    size: count,
    color: colorGradient.getColor(count),
  });

  for (let node of linkStats) {
    nodes.push({
      id: node.entity,
      label: node.entity,
      size: node.count,
      color: colorGradient.getColor(node.count),
    });
  }

  nodes = _.sortBy(nodes, (node) => nodes.id);

  return nodes;
};

const createNetworkEdges = (name, count, linkStats) => {
  let edges = [];

  for (let edge of linkStats) {
    edges.push({
      id: `${name}-${edge.entity}`,
      source: name,
      target: edge.entity,
    });
  }
  return edges;
};

const initialState = {
  name: "",
  boardStats: {},
  linkStats: [],
  edges: [],
  nodes: [],
  count: 0,
  postIds: [],
  posts: [],
  status: {
    requesting: false,
    requestingPosts: false,
  },
};

const entitySlice = createSlice({
  name: "entity",
  initialState,
  reducers: {
    setEntityName: (state, action) => {
      state.name = action.payload;
    },
    requestingEntitySummary: (state) => {
      state.status.requesting = true;
    },
    requestEntitySummarySuccess: (state, action) => {
      const { boardStats, posts, linkStats, count, name } = action.payload;
      state.postsIds = posts;
      state.boardStats = boardStats;
      state.linkStats = linkStats;
      state.count = count;
      state.name = name;
      state.nodes = createNetworkNodes(name, count, linkStats);
      state.edges = createNetworkEdges(name, count, linkStats);
      state.status.requesting = false;
    },
    requestEntitySummaryFailed: (state, action) => {
      state.status.requesting = false;
    },
    requestingEntityPosts: (state) => {
      state.requestingPosts = true;
    },
    requestEntityPostsSuccess: (state, action) => {
      state.posts = action.payload;
      state.requestingPosts = false;
    },
    requestEntityPostsFailed: (state) => {
      state.requestingPosts = false;
    },
  },
});

export const {
  setEntityName,
  requestEntitySummaryFailed,
  requestEntitySummarySuccess,
  requestingEntitySummary,
  requestingEntityPosts,
  requestEntityPostsSuccess,
  requestEntityPostsFailed,
} = entitySlice.actions;

export default entitySlice.reducer;
