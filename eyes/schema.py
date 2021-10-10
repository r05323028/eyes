'''Eyes graphQL schemas module
'''
import graphene
from graphene import Scalar, relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from eyes.db import ptt, stats


class DictType(Scalar):
    '''Graphene dict type
    '''
    @staticmethod
    def serialize(dt):
        '''Serialize method

        Args:
            dt (str)
        '''
        return dt

    @staticmethod
    def parse_literal(node):
        '''Parse literal method

        Args:
            node (relay.Node)
        '''
        return node

    @staticmethod
    def parse_value(value):
        '''Parse value method

        Args:
            value (str)
        '''
        return value


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


class DailySummary(SQLAlchemyObjectType):
    '''Daily summary schema
    '''
    class Meta:
        '''Metadata
        '''
        model = stats.DailySummary
        exclude_fields = ('source', )


class EntitySummary(SQLAlchemyObjectType):
    '''Entity summary
    '''
    board_stats = graphene.List(DictType)
    link_stats = graphene.List(DictType)
    posts = graphene.List(graphene.String)

    class Meta:
        '''Metadata
        '''
        model = stats.EntitySummary
        interfaces = (relay.Node, )


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
    monthly_summaries = graphene.Field(
        graphene.List(MonthSummary),
        source=graphene.Argument(type=graphene.Int, required=True),
        limit=graphene.Argument(type=graphene.Int, required=True),
    )
    daily_summaries = graphene.Field(
        graphene.List(DailySummary),
        source=graphene.Argument(type=graphene.Int, required=True),
        limit=graphene.Argument(type=graphene.Int, required=True),
    )
    entity_summary = graphene.Field(
        EntitySummary,
        name=graphene.Argument(type=graphene.String, required=True),
    )

    def resolve_monthly_summary(self, info, source, year, month):
        '''Resolve monthly summary

        Args:
            source (int)
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

    def resolve_monthly_summaries(self, info, source, limit):
        '''Resolve monthly summaries

        Args:
            source (int)
            limit (int)

        Returns:
            List[stats.MonthlySummary]
        '''
        query = MonthSummary.get_query(info)
        return query.filter(stats.MonthlySummary.source == source).order_by(
            stats.MonthlySummary.year.desc(),
            stats.MonthlySummary.month.desc(),
        ).limit(limit)

    def resolve_daily_summaries(self, info, source, limit):
        '''Resolve daily summaries

        Args:
            source (int)
            last (int)

        Returns:
            List[stats.DailySummary]
        '''
        query = DailySummary.get_query(info)

        return query.filter(stats.DailySummary.source == source, ).order_by(
            stats.DailySummary.year.desc(),
            stats.DailySummary.month.desc(),
            stats.DailySummary.day.desc(),
        ).limit(limit).all()

    def resolve_entity_summary(self, info, name):
        '''Resolve entity summary

        Args:
            name (str)

        Returns:
            stats.EntitySummary
        '''
        query = EntitySummary.get_query(info)
        return query.filter(stats.EntitySummary.name == name).first()


schema = graphene.Schema(query=Query)
