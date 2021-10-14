import { ApolloClient, InMemoryCache } from "@apollo/client";

import {
  ALL_ENTITY_SUMMARIES,
  ALL_PTT_ARTICLES,
  DAILY_SUMMARIES,
  ENTITY_SUMMARY,
  MONTH_SUMMARY,
} from "./query";

export const client = new ApolloClient({
  uri: "http://127.0.0.1:8000/graphql",
  cache: new InMemoryCache(),
});

export async function fetchPTTArticles({ first, before, after, last }) {
  const { data } = await client.query({
    query: ALL_PTT_ARTICLES,
    variables: { first, before, after, last },
  });
  return {
    articles: data.allPttPosts.edges.map((row) => row.node),
    pageInfo: data.allPttPosts.pageInfo,
  };
}

export async function fetchMonthlySummary({ source, year, month }) {
  const { data } = await client.query({
    query: MONTH_SUMMARY,
    variables: { source, year, month },
  });
  return data.monthlySummary;
}

export async function fetchDailySummaries({ source, limit }) {
  const { data } = await client.query({
    query: DAILY_SUMMARIES,
    variables: { source, limit },
  });
  return data.dailySummaries;
}

export async function fetchAllStatsEntitySummaries({ minCount, limit }) {
  const now = new Date();
  const { data } = await client.query({
    query: ALL_ENTITY_SUMMARIES,
    variables: {
      year: now.getFullYear(),
      month: now.getMonth() + 1,
      minCount,
      limit,
    },
  });
  return data.allStatsEntitySummaries;
}

export async function fetchEntitySummary({ name }) {
  const now = new Date();
  const { data } = await client.query({
    query: ENTITY_SUMMARY,
    variables: {
      name: name,
      year: now.getFullYear(),
      month: now.getMonth() + 1,
    },
  });
  return data.entitySummary;
}
