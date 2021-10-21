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
          postId
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
      totalPosts
      totalComments
      year
      month
    }
  }
`;

export const DAILY_SUMMARIES = gql`
  query DailySummaries($source: Int!, $limit: Int!) {
    dailySummaries(source: $source, limit: $limit) {
      year
      month
      day
      totalPosts
    }
  }
`;

export const ALL_ENTITY_SUMMARIES = gql`
  query AllStatsEntitySummaries(
    $year: Int!
    $month: Int!
    $minCount: Int!
    $limit: Int!
  ) {
    allStatsEntitySummaries(
      year: $year
      month: $month
      minCount: $minCount
      limit: $limit
    ) {
      id
      name
      count
      linkStats
    }
  }
`;

export const ENTITY_SUMMARY = gql`
  query EntitySummary($name: String!, $year: Int, $month: Int) {
    entitySummary(name: $name, year: $year, month: $month) {
      id
      name
      count
      boardStats
      linkStats
      posts
    }
  }
`;

export const PTT_POST = gql`
  query PttPost($postId: String!) {
    pttPost(postId: $postId) {
      id
      title
      author
      board
      content
      comments {
        id
        commentId
        author
        reaction
        content
      }
    }
  }
`;

export const PTT_POSTS = gql`
  query PttPosts($postIds: [String]!) {
    pttPosts(postIds: $postIds) {
      id
      postId
      title
      author
      board
      content
      createdAt
    }
  }
`;
