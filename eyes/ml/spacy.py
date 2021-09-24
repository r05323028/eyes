'''Eyes ml spacy module
'''
from typing import Dict

from spacy.language import Language
from spacy.tokens import Doc

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


def binary_to_doc(
    binary: bytes,
    nlp: Language,
) -> Doc:
    '''Transform bytes to spacy doc

    Args:
        binary (bytes): spacy binary string
        nlp (Language): spacy language model

    Returns:
        Doc: spacy doc
    '''
    return Doc(nlp.vocab).from_bytes(binary)


def transform_ptt_comment(
    comment: spacy.SpacyPttComment,
    nlp: Language,
) -> Dict:
    '''Transform ptt comment to decoded dictionary

    Args:
        comment (spacy.SpacyPttComment): spacy binary comment
        nlp (Language): spacy language model

    Returns:
        Dict: decoded dictionary
    '''
    return {
        'comment_id': comment.comment_id,
        'post_id': comment.post_id,
        'content': binary_to_doc(comment.content, nlp),
    }


def transform_ptt_post(
    post: spacy.SpacyPttPost,
    nlp: Language,
) -> Dict:
    '''Transform ptt post to decoded dictionary

    Args:
        post (spacy.SpacyPttPost): spacy binary post
        nlp (Language): spacy language model

    Returns:
        Dict: decoded dictionary
    '''
    return {
        'id': post.id,
        'title': binary_to_doc(post.title, nlp),
        'content': binary_to_doc(post.content, nlp),
        'comments':
        [transform_ptt_comment(comment, nlp) for comment in post.comments],
    }
