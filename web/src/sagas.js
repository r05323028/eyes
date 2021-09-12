import { put, call, all, takeEvery } from "redux-saga/effects";
import { createAction } from "@reduxjs/toolkit";
import {
  requestArticlesFailed,
  requestArticlesSuccess,
  requestingArticles,
  setCurrentPage,
  requestingMonthlySummary,
  requestMonthlySummarySuccess,
  requestMonthlySummaryFailed,
  requestingDailySummaries,
  requestDailySummariesSuccess,
  requestDailySummariesFailed,
} from "./reducers/article";

import {
  fetchPTTArticles,
  fetchMonthlySummary,
  fetchDailySummaries,
} from "./api";

export const sagaActions = {
  requestPTTArticles: createAction("articles/requestPTTArticlesSaga"),
  requestPTTArticlesNextPage: createAction(
    "articles/requestPTTArticlesNextPageSaga"
  ),
  requestPTTArticlesPreviousPage: createAction(
    "articles/requestPTTArticlesPreviousPageSaga"
  ),
  requestPTTMonthlySummary: createAction("article/requestPTTMonthlySummary"),
  requestPTTDailySummaries: createAction("article/requestPTTDailySummaries"),
};

function* requestPTTArticlesSaga(action) {
  try {
    yield put(requestingArticles());
    const articles = yield call(fetchPTTArticles, { first: 10 });
    yield put(requestArticlesSuccess(articles));
  } catch (err) {
    yield put(requestArticlesFailed());
  }
}

function* requestPTTArticlesNextPageSaga(action) {
  const pageInfo = action.payload;
  try {
    yield put(requestingArticles());
    const articles = yield call(fetchPTTArticles, {
      first: 10,
      after: pageInfo.endCursor,
    });
    yield put(requestArticlesSuccess(articles));
    yield put(setCurrentPage(1));
  } catch (err) {
    yield put(requestArticlesFailed());
  }
}

function* requestPTTArticlesPreviousPageSaga(action) {
  const pageInfo = action.payload;
  try {
    yield put(requestingArticles());
    const articles = yield call(fetchPTTArticles, {
      last: 10,
      before: pageInfo.startCursor,
    });
    yield put(requestArticlesSuccess(articles));
    yield put(setCurrentPage(-1));
  } catch (err) {
    yield put(requestArticlesFailed());
  }
}

function* requestPTTMonthlySummarySaga(action) {
  const { source, year, month } = action.payload;
  try {
    yield put(requestingMonthlySummary());
    const monthlySummary = yield call(fetchMonthlySummary, {
      source,
      year,
      month,
    });
    yield put(requestMonthlySummarySuccess(monthlySummary));
  } catch (err) {
    yield put(requestMonthlySummaryFailed());
  }
}

function* requestPTTDailySummariesSaga(action) {
  const { source, limit } = action.payload;
  try {
    yield put(requestingDailySummaries());
    const dailySummaries = yield call(fetchDailySummaries, {
      source,
      limit,
    });
    yield put(requestDailySummariesSuccess(dailySummaries));
  } catch (err) {
    yield put(requestDailySummariesFailed());
  }
}

export default function* rootSaga() {
  yield all([
    takeEvery(sagaActions.requestPTTArticles, requestPTTArticlesSaga),
    takeEvery(
      sagaActions.requestPTTArticlesNextPage,
      requestPTTArticlesNextPageSaga
    ),
    takeEvery(
      sagaActions.requestPTTArticlesPreviousPage,
      requestPTTArticlesPreviousPageSaga
    ),
    takeEvery(
      sagaActions.requestPTTMonthlySummary,
      requestPTTMonthlySummarySaga
    ),
    takeEvery(
      sagaActions.requestPTTDailySummaries,
      requestPTTDailySummariesSaga
    ),
  ]);
}
