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
  requestingPost,
  requestPostSuccess,
  requestPostFailed,
} from "./reducers/article";
import {
  requestingAllStatsEntitySummaries,
  requestAllStatsEntitySummariesSuccess,
  requestAllStatsEntitySummariesFailed,
} from "./reducers/entities";
import {
  requestingEntitySummary,
  requestEntitySummarySuccess,
  requestEntitySummaryFailed,
} from "./reducers/entity";

import {
  fetchPTTArticles,
  fetchMonthlySummary,
  fetchDailySummaries,
  fetchAllStatsEntitySummaries,
  fetchEntitySummary,
  fetchPttPost,
} from "./api";

import { NODE_MIN_COUNT } from "./constant";

export const sagaActions = {
  requestPTTArticles: createAction("articles/requestPTTArticlesSaga"),
  requestPTTArticlesNextPage: createAction(
    "articles/requestPTTArticlesNextPageSaga"
  ),
  requestPTTArticlesPreviousPage: createAction(
    "articles/requestPTTArticlesPreviousPageSaga"
  ),
  requestPTTMonthlySummary: createAction(
    "article/requestPTTMonthlySummarySaga"
  ),
  requestPTTDailySummaries: createAction(
    "article/requestPTTDailySummariesSaga"
  ),
  requestAllStatsEntitySummaries: createAction(
    "entities/requestAllStatsEntitySummariesSaga"
  ),
  requestEntitySummary: createAction("entity/requestEntitySummarySaga"),
  requestPost: createAction("post/requestPostSaga"),
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

function* requestAllStatsEntitySummariesSaga(action) {
  const { limit } = action.payload;
  const minCount = NODE_MIN_COUNT;
  try {
    yield put(requestingAllStatsEntitySummaries());
    const allStatsEntitySummaries = yield call(fetchAllStatsEntitySummaries, {
      limit,
      minCount,
    });
    yield put(requestAllStatsEntitySummariesSuccess(allStatsEntitySummaries));
  } catch (err) {
    yield put(requestAllStatsEntitySummariesFailed());
  }
}

function* requestEntitySummarySaga(action) {
  const { name } = action.payload;
  try {
    yield put(requestingEntitySummary());
    const entitySummary = yield call(fetchEntitySummary, { name });
    yield put(requestEntitySummarySuccess(entitySummary));
  } catch (err) {
    yield put(requestEntitySummaryFailed());
  }
}

function* requestPostSaga(action) {
  const { postId } = action.payload;
  try {
    yield put(requestingPost());
    const post = yield call(fetchPttPost, { postId });
    yield put(requestPostSuccess(post));
  } catch (err) {
    yield put(requestPostFailed());
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
    takeEvery(
      sagaActions.requestAllStatsEntitySummaries,
      requestAllStatsEntitySummariesSaga
    ),
    takeEvery(sagaActions.requestEntitySummary, requestEntitySummarySaga),
    takeEvery(sagaActions.requestPost, requestPostSaga),
  ]);
}
