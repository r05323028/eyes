'''Eyes graphQL schemas module
'''
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from eyes.db import ptt


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


class Query(graphene.ObjectType):
    '''GraphQL Query definitions
    '''
    node = relay.Node.Field()
    all_ptt_posts = SQLAlchemyConnectionField(PttPost.connection)


schema = graphene.Schema(query=Query)
