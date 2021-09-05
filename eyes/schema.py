'''Eyes graphQL schemas module
'''
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

import eyes.db as db


class PttComment(SQLAlchemyObjectType):
    '''Ptt comment GraphQL schema
    '''
    class Meta:
        '''Metadata
        '''
        model = db.PttComment
        interfaces = (relay.Node, )


class PttPost(SQLAlchemyObjectType):
    '''Ptt post GraphQL schema
    '''
    class Meta:
        '''Metadata
        '''
        model = db.PttPost
        interfaces = (relay.Node, )

    comments = graphene.List(PttComment)


class Query(graphene.ObjectType):
    '''GraphQL Query definitions
    '''
    node = relay.Node.Field()
    all_ptt_posts = SQLAlchemyConnectionField(PttPost.connection)


schema = graphene.Schema(query=Query)
