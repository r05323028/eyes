'''Eyes label functions module
'''
import logging
from collections import defaultdict
from typing import Dict, List

from rich.logging import RichHandler
from skweak.base import CombinedAnnotator
from skweak.gazetteers import GazetteerAnnotator, Trie
from sqlalchemy.orm import Session

from eyes.data import Entity
from eyes.db.wiki import WikiEntity
from eyes.type import Label

logger = logging.getLogger(__name__)
logger.addHandler(RichHandler(rich_tracebacks=True))
logger.setLevel(logging.INFO)


def build_tries(entities: List[Entity]) -> Dict[str, Trie]:
    '''Build Gazetteer Tries

    Args:
        entities (List[Entity]): entities

    Returns:
        Dict[str, Trie]: tries used in gazetteer
    '''
    tries = defaultdict(list)
    labels = set()
    for ent in entities:
        tries[ent.label.name].append([ent.name])
        if ent.label.name not in labels:
            labels.add(ent.label.name)
    for label in labels:
        tries[label] = Trie(tries[label])
    return tries


class NERAnnotator(CombinedAnnotator):
    '''NER Annotator for spacy document
    '''
    def __init__(self, sess: Session):
        super(NERAnnotator, self).__init__()
        self.sess = sess

    def add_all(self):
        '''Add all annotators
        '''
        logger.info("Loading Gazetteer Annotators")
        self.add_gazetteers()

    def add_gazetteers(self):
        '''Add gazetteers to annotator
        '''
        rows = self.sess.query(WikiEntity).filter(
            WikiEntity.label == Label['PERSON']).all()
        entities = [
            Entity(
                name=row.name,
                type=row.type,
                alias=row.alias,
                label=row.label,
            ) for row in rows
        ]
        tries = build_tries(entities)
        self.add_annotator(GazetteerAnnotator('person_wiki', tries))
