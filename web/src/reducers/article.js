import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  currentTab: "PTT",
  articles: [],
  pageInfo: {},
  currentPage: 1,
  status: {
    requesting: false,
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
  },
});

export const {
  setCurrentTab,
  setCurrentPage,
  requestingArticles,
  requestArticlesFailed,
  requestArticlesSuccess,
} = articleSlice.actions;

export default articleSlice.reducer;
