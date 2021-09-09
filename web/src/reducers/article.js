import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  currentTab: "PTT",
  monthlySummary: {},
  articles: [],
  pageInfo: {},
  currentPage: 1,
  status: {
    requesting: false,
    requestingSummary: false,
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
      state.status.requestingSummary = true;
    },
    requestMonthlySummarySuccess: (state, action) => {
      state.status.requestingSummary = false;
      state.monthlySummary = action.payload;
    },
    requestMonthlySummaryFailed: (state, action) => {
      state.status.requestingSummary = false;
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
} = articleSlice.actions;

export default articleSlice.reducer;
