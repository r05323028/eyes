import { gql } from "@apollo/client";

export const ALL_PTT_ARTICLES = gql`
  query AllPTTPosts($first: Int, $before: String, $after: String, $last: Int) {
    allPttPosts(
      first: $first
      last: $last
      sort: CREATED_AT_DESC
      before: $before
      after: $after
    ) {
      pageInfo {
        startCursor
        endCursor
        hasNextPage
        hasPreviousPage
      }
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

export const MONTH_SUMMARY = gql`
  query MonthlySummary($source: Int!, $year: Int!, $month: Int!) {
    monthlySummary(source: $source, year: $year, month: $month) {
      source
      totalPosts
      totalComments
      year
      month
    }
  }
`;
