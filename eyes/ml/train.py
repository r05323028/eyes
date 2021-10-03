'''Eyes train module
'''
from typing import Iterable

from rich.progress import Progress
from spacy.language import Language
from spacy.tokens import Doc
from sqlalchemy.orm import Session

from eyes.db import ptt
from eyes.ml.lf import NERAnnotator


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
