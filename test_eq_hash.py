from model import Batch
from collections import Counter


def test_유일한_해쉬값인_reference가_같을_때_집합_에서_동일하게_인식_되는_예제():
    A = Batch('1', '2', 3, None)
    B = Batch('1', '4', 5, None)
    assert len(set([A, B])) == 1


def test_유일한_해쉬값인_reference가_같을_때_딕셔너리_키_값이_동일하게_인식_되는_예제():
    A = Batch('1', '2', 3, None)
    B = Batch('1', '4', 5, None)
    assert len(Counter([A, B]).keys()) == 1
