from datetime import datetime
from chapter_01.model import Batch, OrderLine, allocate, OutOfStock
from pytest import raises

def test_배치_리스트_eta가_없을_때_먼저_할당_되는_지_확인():
    batch = Batch('batch-001', 'clock', 100, eta=None)
    eta_batch = Batch('batch-002', 'clock', 100, eta=datetime.now())
    line = OrderLine('oref', 'clock', 10)

    allocate(line, [batch, eta_batch])

    assert batch.available_quantity == 90
    assert eta_batch.available_quantity == 100


def test_배치_리스트_eta_순으로_정렬되어_할당_되는_지_확인():
    earliest = Batch('batch-001', 'clock', 100, eta=None)
    medium = Batch('batch-002', 'clock', 100, eta=datetime(year=2011, month=1, day=1))
    latest = Batch('batch-003', 'clock', 100, eta=datetime(year=2012, month=1, day=1))

    line = OrderLine('oref', 'clock', 10)
    allocate(line, [earliest, medium, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_allocate_함수_리턴값_확인():
    batch = Batch('batch-001', 'clock', 100, eta=None)
    eta_batch = Batch('batch-002', 'clock', 100, eta=datetime.now())
    line = OrderLine('oref', 'clock', 10)

    assert batch.id == allocate(line, [batch, eta_batch])


def test_allocate_함수_품절_예외_테스트():
    batch = Batch('batch1', 'fork', 10, eta=datetime.today())
    allocate(OrderLine('order1', 'fork', 10), [batch])

    with raises(OutOfStock, match='fork'):
        allocate(OrderLine('order2', 'fork', 10), [batch])
