import { put, call, all, takeEvery } from "redux-saga/effects";
import { createAction } from "@reduxjs/toolkit";
import {
  requestArticlesFailed,
  requestArticlesSuccess,
  requestingArticles,
} from "./reducers/article";

import { fetchPTTArticles } from "./api";

export const sagaActions = {
  requestPTTArticles: createAction("articles/requestPTTArticlesSaga"),
};

function* requestPTTArticlesSaga(action) {
  try {
    yield put(requestingArticles());
    const articles = yield call(fetchPTTArticles);
    yield put(requestArticlesSuccess(articles));
  } catch (err) {
    yield put(requestArticlesFailed());
  }
}

export default function* rootSaga() {
  yield all([
    takeEvery(sagaActions.requestPTTArticles, requestPTTArticlesSaga),
  ]);
}
