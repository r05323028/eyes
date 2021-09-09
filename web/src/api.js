import { ApolloClient, InMemoryCache } from "@apollo/client";

import { ALL_PTT_ARTICLES } from "./query";

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
