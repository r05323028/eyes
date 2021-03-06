import { configureStore } from "@reduxjs/toolkit";
import { articleSlice, entitiesSlice, entitySlice } from "./reducers";
import createSagaMiddleware from "@redux-saga/core";
import sagas from "./sagas";

const sagaMiddleware = createSagaMiddleware();

const store = configureStore({
  reducer: {
    article: articleSlice,
    entities: entitiesSlice,
    entity: entitySlice,
  },
  devTools: process.env.NODE_ENV === "development",
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({ thunk: false }).concat(sagaMiddleware),
});

sagaMiddleware.run(sagas);

export default store;
