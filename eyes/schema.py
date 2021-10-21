'''Eyes graphQL schemas module
'''
from datetime import datetime

import graphene
from graphene import Scalar, relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from eyes.db import ptt, stats, wiki


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


class WikiEntity(SQLAlchemyObjectType):
    '''Wiki entity
    '''
    alias = graphene.List(graphene.String)

    class Meta:
        '''Metadata
        '''
        model = wiki.WikiEntity
        exclude_fields = ('label', 'alias')
        interfaces = (relay.Node, )


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
    all_wiki_entities = SQLAlchemyConnectionField(WikiEntity.connection)
    all_stats_entity_summaries = graphene.Field(
        graphene.List(EntitySummary),
        year=graphene.Argument(type=graphene.Int),
        month=graphene.Argument(type=graphene.Int),
        min_count=graphene.Argument(type=graphene.Int, default_value=1),
        limit=graphene.Argument(type=graphene.Int),
    )
    ptt_post = graphene.Field(
        PttPost,
        post_id=graphene.Argument(type=graphene.String, required=True),
    )
    ptt_posts = graphene.Field(
        graphene.List(PttPost),
        post_ids=graphene.Argument(
            type=graphene.List(graphene.String),
            required=True,
        ),
    )
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
        year=graphene.Argument(type=graphene.Int,
                               default_value=datetime.now().year),
        month=graphene.Argument(type=graphene.Int,
                                default_value=datetime.now().month),
    )

    def resolve_ptt_post(self, info, post_id):
        '''Resolve ptt post

        Args:
            post_id (str): PTT post id

        Returns:
            ptt.PttPost
        '''
        query = PttPost.get_query(info)
        return query.filter(ptt.PttPost.id == post_id, ).first()

    def resolve_ptt_posts(self, info, post_ids):
        '''Resolve ptt posts

        Args:
            post_ids (List[str]): Ptt post ids

        Returns:
            List[ptt.PttPost]
        '''
        query = PttPost.get_query(info)
        return query.filter(ptt.PttPost.id.in_(post_ids)).order_by(
            ptt.PttPost.created_at)

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

    def resolve_entity_summary(self, info, name, year, month):
        '''Resolve entity summary

        Args:
            name (str)
            year (int)
            month (int)

        Returns:
            stats.EntitySummary
        '''
        query = EntitySummary.get_query(info)
        return query.filter(
            stats.EntitySummary.name == name,
            stats.EntitySummary.year == year,
            stats.EntitySummary.month == month,
        ).first()

    def resolve_all_stats_entity_summaries(self, info, year, month, min_count,
                                           limit):
        '''Resolve all stats entity summary

        Args:
            year (int): Year
            month (int): Month
            limit (int): Max number of entities

        Returns:
            List[stats.EntitySummary]
        '''
        query = EntitySummary.get_query(info)
        query = query.filter(
            stats.EntitySummary.year == year,
            stats.EntitySummary.month == month,
            stats.EntitySummary.count > min_count,
        ).order_by(stats.EntitySummary.count.desc())
        if limit:
            query = query.limit(limit)
        return query.all()


schema = graphene.Schema(query=Query)
