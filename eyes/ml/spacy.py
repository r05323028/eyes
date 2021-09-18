'''Eyes ml spacy module
'''
from spacy.language import Language

from eyes.data import spacy
from eyes.db import ptt


def transform_ptt_post_to_spacy(
    post: ptt.PttPost,
    nlp: Language,
) -> spacy.SpacyPttPost:
    '''Transform ptt post to spacy doc binary

    Args:
        post (ptt.PttPost):

    Returns:
        spacy.SpacyPttPost
    '''
    title_bytes = nlp(post.title).to_bytes()
    content_bytes = nlp(post.content).to_bytes()
    comments = []
    for comment in post.comments:
        comment_bytes = nlp(comment.content).to_bytes()
        comments.append(
            spacy.SpacyPttComment(
                comment_id=comment.comment_id,
                post_id=comment.post_id,
                content=comment_bytes,
            ))

    return spacy.SpacyPttPost(
        id=post.id,
        title=title_bytes,
        content=content_bytes,
        comments=comments,
    )
