import { gql } from "@apollo/client";

export const ALL_PTT_ARTICLES = gql`
  query AllPTTPosts($last: Int!) {
    allPttPosts(last: $last) {
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
