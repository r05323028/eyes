import _ from "lodash";
import Gradient from "javascript-color-gradient";
import { createSlice } from "@reduxjs/toolkit";
import { EDGE_MIN_COUNT } from "../constant";

const colorGradient = new Gradient();
colorGradient.setGradient("#2D8BD7", "#D70650");
colorGradient.setMidpoint(300);

const initialState = {
  allStatsEntitySummaries: [],
  edges: [],
  nodes: [],
  currentEntity: "",
  status: {
    requesting: false,
    loaded: false,
  },
};

const createNetworkData = (data) => {
  const nodes = _.map(data, (ent) => {
    return {
      id: ent.name,
      label: ent.name,
      size: ent.count,
    };
  });

  // other nodes
  let otherNodes = [];
  for (let row of data) {
    for (let node of row.linkStats) {
      let idx = _.findIndex(otherNodes, { name: node.entity });
      if (idx === -1) {
        otherNodes.push({
          name: node.entity,
          count: 1,
        });
      } else {
        const obj = otherNodes[idx];
        obj.count += 1;
      }
    }
  }
  otherNodes = _.map(otherNodes, (node) => {
    return {
      id: node.name,
      label: node.name,
      size: node.count,
    };
  });
  let finalNodes = _([...nodes, ...otherNodes])
    .groupBy("id")
    .map((value, key) => {
      let sum = _.sumBy(value, "size");
      return {
        id: key,
        label: key,
        size: sum,
        color: colorGradient.getColor(sum),
      };
    })
    .value();

  // edges
  let edges = [];
  for (let row of data) {
    for (let node of row.linkStats) {
      if (node.count > EDGE_MIN_COUNT) {
        edges.push({
          id: `${row.name}-${node.entity}`,
          source: row.name,
          target: node.entity,
          count: node.count,
        });
      }
    }
  }

  return { nodes: finalNodes, edges };
};

const entitiesSlice = createSlice({
  name: "entities",
  initialState,
  reducers: {
    requestingAllStatsEntitySummaries: (state) => {
      state.status.requesting = true;
    },
    requestAllStatsEntitySummariesSuccess: (state, action) => {
      state.status.requesting = false;
      state.allStatsEntitySummaries = action.payload;
      const { nodes, edges } = createNetworkData(action.payload);
      state.nodes = nodes;
      state.edges = edges;
      state.status.loaded = true;
    },
    requestAllStatsEntitySummariesFailed: (state) => {
      state.status.requesting = false;
    },
    setCurrentEntity: (state, action) => {
      const { currentEntity } = action.payload;
      state.currentEntity = currentEntity;
    },
  },
});

export const {
  requestingAllStatsEntitySummaries,
  requestAllStatsEntitySummariesSuccess,
  requestAllStatsEntitySummariesFailed,
  setCurrentEntity,
} = entitiesSlice.actions;

export default entitiesSlice.reducer;
