'''Eyes spacy data container
'''
from typing import Dict, List

from pydantic import BaseModel, Field
from spacy.language import Language

from eyes.db import spacy as spacy_orm


class SpacyPttComment(BaseModel):
    '''Spacy ptt comment data container
    '''
    comment_id: int
    post_id: str
    content: bytes

    class Config:
        orm_mode = True

    def to_orm(self) -> spacy_orm.SpacyPttComment:
        '''Transform to orm model

        Returns:
            spacy.SpacyPttComment
        '''
        return spacy_orm.SpacyPttComment(
            comment_id=self.comment_id,
            post_id=self.post_id,
            content=self.content,
        )


class SpacyPttPost(BaseModel):
    '''Spacy ptt post data container
    '''
    id: str
    title: bytes
    content: bytes
    comments: List[SpacyPttComment] = Field([])

    class Config:
        orm_mode = True

    def to_orm(self) -> spacy_orm.SpacyPttPost:
        '''Transform to orm model

        Returns:
            spacy.SpacyPttPost
        '''
        return spacy_orm.SpacyPttPost(
            id=self.id,
            title=self.title,
            content=self.content,
            comments=[com.to_orm() for com in self.comments],
        )
