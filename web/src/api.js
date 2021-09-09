import { ApolloClient, InMemoryCache } from "@apollo/client";

import { ALL_PTT_ARTICLES, MONTH_SUMMARY } from "./query";

export const client = new ApolloClient({
  uri: "http://localhost:8000/graphql",
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
