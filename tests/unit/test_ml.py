'''Tests of ml module
'''
from typing import Dict

from skweak.gazetteers import Trie

from eyes.data import Entity
from eyes.ml.lf import build_tries
from eyes.type import Label


class TestLf:
    '''Test cases of lf module
    '''        
    def test_build_trie(self):
        '''Test build trie
        '''
        entities = [
            Entity(
                name='張惠妹',
                label=Label['PERSON'],
            ),
            Entity(
                name='周杰倫',
                label=Label['PERSON'],
            )
        ]
        tries = build_tries(entities)
        assert isinstance(tries, Dict)
