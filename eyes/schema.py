'''Eyes graphQL schemas module
'''
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from eyes.db import ptt, stats


class PttComment(SQLAlchemyObjectType):
    '''Ptt comment GraphQL schema
    '''
    class Meta:
        '''Metadata
        '''
        model = ptt.PttComment
        interfaces = (relay.Node, )


class PttPost(SQLAlchemyObjectType):
    '''Ptt post GraphQL schema
    '''
    class Meta:
        '''Metadata
        '''
        model = ptt.PttPost
        interfaces = (relay.Node, )

    comments = graphene.List(PttComment)


class MonthSummary(SQLAlchemyObjectType):
    '''Monthly summary schema
    '''
    class Meta:
        '''Metadata
        '''
        model = stats.MonthlySummary
        exclude_fields = ('source', )


class Query(graphene.ObjectType):
    '''GraphQL Query definitions
    '''
    node = relay.Node.Field()
    all_ptt_posts = SQLAlchemyConnectionField(PttPost.connection)
    monthly_summary = graphene.Field(
        MonthSummary,
        source=graphene.Argument(type=graphene.Int, required=True),
        year=graphene.Argument(type=graphene.Int, required=True),
        month=graphene.Argument(type=graphene.Int, required=True),
    )

    def resolve_monthly_summary(self, info, source, year, month):
        '''Resolve monthly summary

        Args:
            source (SourceType)
            year (int)
            month (int)

        Returns:
            stats.MonthlySummary
        '''
        query = MonthSummary.get_query(info)
        return query.filter(
            stats.MonthlySummary.source == source,
            stats.MonthlySummary.year == year,
            stats.MonthlySummary.month == month,
        ).first()


schema = graphene.Schema(query=Query)
