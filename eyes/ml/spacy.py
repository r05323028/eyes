'''Eyes ml spacy module
'''
from typing import Dict, Iterable

from rich.progress import Progress
from spacy.language import Language
from spacy.tokens import Doc
from sqlalchemy.orm import Session

from eyes.data import spacy
from eyes.db import ptt
from eyes.ml.lf import NERAnnotator


def transform_ptt_post_to_spacy(
    post: ptt.PttPost,
    nlp: Language,
    disable: Iterable[str] = ['tok2vec'],
) -> spacy.SpacyPttPost:
    '''Transform ptt post to spacy doc binary

    Args:
        post (ptt.PttPost): ptt post
        nlp (Language): spacy language model
        disable (Iterable[str]): disabled pipeline

    Returns:
        spacy.SpacyPttPost
    '''
    title_bytes = nlp(post.title, disable=disable).to_bytes()
    content_bytes = nlp(post.content, disable=disable).to_bytes()
    comments = []
    for comment in post.comments:
        comment_bytes = nlp(comment.content, disable=disable).to_bytes()
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
        'id':
        post.id,
        'title':
        binary_to_doc(post.title, nlp),
        'content':
        binary_to_doc(post.content, nlp),
        'comments':
        [transform_ptt_comment(comment, nlp) for comment in post.comments],
    }


def build_docs(
    nlp: Language,
    sess: Session,
    limit: int = 100000,
    batch_size: int = 32,
) -> Iterable[Doc]:
    '''Build spacy docs

    Args:
        sess (Session): sqlalchemy session
        limit (int): max number of docs

    Returns:
        Iterable[Doc]: spacy docs
    '''
    docs = []
    start = 0
    annotator = NERAnnotator(sess)
    annotator.add_all()
    query = sess.query(ptt.PttPost).order_by(ptt.PttPost.created_at.desc())
    with Progress() as progress:
        task = progress.add_task('[red]Building Docs...', total=limit)
        while not progress.finished:
            stop = start + batch_size
            batch_docs = []
            for row in query.slice(start, stop):
                title = row.title
                content = row.content
                comments = [com.content for com in row.comments]
                comments = '\n'.join(comments)
                doc = nlp('\n'.join([title, content, comments]))
                doc = annotator(doc)
                batch_docs.append(doc)
            for doc in batch_docs:
                doc.ents = doc.spans['person_wiki']
            batch_docs = [doc for doc in batch_docs if len(doc.ents) > 0]
            docs.extend(batch_docs)
            progress.update(task, advance=len(batch_docs))
            start += batch_size
    return docs
