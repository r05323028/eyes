import _ from "lodash";
import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  currentTab: "PTT",
  currentPost: {},
  monthlySummary: {},
  dailySummaries: [],
  articles: [],
  pageInfo: {},
  currentPage: 1,
  status: {
    requesting: false,
    requestingMonthlySummary: false,
    requestingDailySummaries: false,
    requestingPost: false,
    modalOpen: false,
  },
};

const articleSlice = createSlice({
  name: "article",
  initialState,
  reducers: {
    setCurrentPage: (state, action) => {
      state.currentPage += action.payload;
    },
    setCurrentTab: (state, action) => {
      state.currentTab = action.payload;
    },
    requestingArticles: (state, action) => {
      state.status.requesting = true;
    },
    requestArticlesSuccess: (state, action) => {
      const { articles, pageInfo } = action.payload;
      state.status.requesting = false;
      state.articles = articles;
      state.pageInfo = pageInfo;
    },
    requestArticlesFailed: (state, action) => {
      state.status.requesting = false;
    },
    requestingMonthlySummary: (state, action) => {
      state.status.requestingMonthlySummary = true;
    },
    requestMonthlySummarySuccess: (state, action) => {
      state.status.requestingMonthlySummary = false;
      state.monthlySummary = action.payload;
    },
    requestMonthlySummaryFailed: (state, action) => {
      state.status.requestingMonthlySummary = false;
    },
    requestingDailySummaries: (state, action) => {
      state.status.requestingDailySummaries = true;
    },
    requestDailySummariesSuccess: (state, action) => {
      state.status.requestingDailySummaries = false;
      state.dailySummaries = _.sortBy(
        action.payload,
        (row) => new Date(row.year, row.month, row.day)
      );
    },
    requestDailySummariesFailed: (state, action) => {
      state.status.requestingDailySummaries = false;
    },
    requestingPost: (state) => {
      state.status.requestingPost = true;
      state.currentPost = {};
    },
    requestPostSuccess: (state, action) => {
      state.currentPost = action.payload;
      state.status.requestingPost = false;
    },
    requestPostFailed: (state) => {
      state.status.requestingPost = false;
    },
    setModalOpen: (state, action) => {
      state.status.modalOpen = action.payload;
    },
  },
});

export const {
  setCurrentTab,
  setCurrentPage,
  requestingArticles,
  requestArticlesFailed,
  requestArticlesSuccess,
  requestingMonthlySummary,
  requestMonthlySummarySuccess,
  requestMonthlySummaryFailed,
  requestingDailySummaries,
  requestDailySummariesSuccess,
  requestDailySummariesFailed,
  requestingPost,
  requestPostSuccess,
  requestPostFailed,
  setModalOpen,
} = articleSlice.actions;

export default articleSlice.reducer;
