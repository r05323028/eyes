import { gql } from "@apollo/client";

export const ALL_PTT_ARTICLES = gql`
  query AllPTTPosts($first: Int!) {
    allPttPosts(first: $first, sort: CREATED_AT_DESC) {
      edges {
        node {
          id
          title
          author
          board
          numComments
          createdAt
        }
      }
    }
  }
`;
