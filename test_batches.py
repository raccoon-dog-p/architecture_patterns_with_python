from datetime import datetime
from chapter_01.model import Batch, OrderLine


def make_batch_and_line(sku: str, batch_qty: int, line_qty: int):
    return (
        Batch('batch-001', sku, batch_qty, datetime.today()),
        OrderLine('order-123', sku, line_qty)
    )


def test_배치_수량이_라인_수량보다_클_때_할당_가능_여부():
    large_batch, small_line = make_batch_and_line('LAMP', 20, 2)
    assert large_batch.is_allocate(small_line)


def test_배치_수량이_라인_수량보다_적을_때_할당_가능_여부():
    small_batch, large_line = make_batch_and_line('LAMP', 2, 20)
    assert small_batch.is_allocate(large_line) is False


def test_배치_수량이_라인_수량과_같을_때_할당_가능_여부():
    equal_batch, eqaul_line = make_batch_and_line('LAMP', 2, 2)
    assert equal_batch.is_allocate(eqaul_line)


def test_배치_SKU와_라인_SKU가_매칭이_안될때():
    batch = Batch('batch-001', 'BIG_SWORD', 20, None)
    different_sku_line = OrderLine('order-123', 'SMALL_SWORD', 20)
    assert batch.is_allocate(different_sku_line) is False


def test_배치에_할당된_라인_해제하였을_때_수량_확인():
    batch, unallocated_line = make_batch_and_line('DECORATIVE_TRINKET', 20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20


def test_할당_멱등성_테스트():
    batch, line = make_batch_and_line('DESK', 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18


def test_Batch_equal():
    batch = Batch('123', 'sword', 20, None)
    assert batch.__eq__(Batch('123', 'gun', 1, None))
