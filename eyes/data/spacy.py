'''Eyes spacy data container
'''
from typing import List

from pydantic import BaseModel, Field

from eyes.db import spacy


class SpacyPttComment(BaseModel):
    '''Spacy ptt comment data container
    '''
    comment_id: int
    post_id: str
    content: bytes

    def to_orm(self) -> spacy.SpacyPttComment:
        '''Transform to orm model

        Returns:
            spacy.SpacyPttComment
        '''
        return spacy.SpacyPttComment(
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

    def to_orm(self) -> spacy.SpacyPttPost:
        '''Transform to orm model

        Returns:
            spacy.SpacyPttPost
        '''
        return spacy.SpacyPttPost(
            id=self.id,
            title=self.title,
            content=self.content,
            comments=[com.to_orm() for com in self.comments],
        )
