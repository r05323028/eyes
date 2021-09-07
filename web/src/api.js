import { ApolloClient, InMemoryCache } from "@apollo/client";

import { ALL_PTT_ARTICLES } from "./query";

export const client = new ApolloClient({
  uri: "http://localhost:8000/graphql",
  cache: new InMemoryCache(),
});

export async function fetchPTTArticles(last = 10) {
  const { data } = await client.query({
    query: ALL_PTT_ARTICLES,
    variables: { last },
  });
  return data.allPttPosts.edges.map((row) => row.node);
}
