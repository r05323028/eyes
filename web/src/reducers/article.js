import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  currentTab: "PTT",
  articles: [],
  status: {
    requesting: false,
  },
};

const articleSlice = createSlice({
  name: "article",
  initialState,
  reducers: {
    setCurrentTab: (state, action) => {
      state.currentTab = action.payload;
    },
    requestingArticles: (state, action) => {
      state.status.requesting = true;
    },
    requestArticlesSuccess: (state, action) => {
      state.status.requesting = false;
      state.articles = action.payload;
    },
    requestArticlesFailed: (state, action) => {
      state.status.requesting = false;
    },
  },
});

export const {
  setCurrentTab,
  requestingArticles,
  requestArticlesFailed,
  requestArticlesSuccess,
} = articleSlice.actions;

export default articleSlice.reducer;
