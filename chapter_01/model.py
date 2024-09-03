from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    quantity: int


class Batch:
    def __init__(
            self,
            id: str,
            sku: str,
            batch_quantity: int,
            eta: Optional[date]):
        self.id = id
        self.sku = sku
        self._batch_quantity = batch_quantity
        self._allocations = set()  # type: set[OrderLine]
        self.eta = eta

    # __eq__ 와 __hash__ 매직메서드를 구현 하면 객체를 집합(set)에 추가하거나 딕셔너리의 키로 접근 가능
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return False
        return other.id == self.id

    # Batch라는 객체는 id가 유일한 해쉬 값이며 이 id가 같다면 동등한 객체로 인식된다.
    # 자세한 사항은 https://docs.python.org/3/reference/datamodel.html#object.__hash__ 해당 docs 참조
    # 간단한 예제는 test_eq_hash.py로 구현
    def __hash__(self) -> int:
        return hash(self.id)

    # Batch라는 객체를 sorted 할 수 있게 만든 매직 메서드, 날짜 순으로 비교한다.
    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, order_line: OrderLine):
        if self.is_allocate(order_line):
            self._allocations.add(order_line)

    def deallocate(self, order_line: OrderLine):
        if order_line in self._allocations:
            self._allocations.remove

    def is_allocate(self, order_line: OrderLine) -> bool:
        if self.sku == order_line.sku and self.available_quantity >= order_line.quantity:
            return True
        else:
            return False

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._batch_quantity - self.allocated_quantity


class OutOfStock(Exception):
    pass

# 도메인 서비스에 대한 단독 함수
def allocate(line: OrderLine, batches: list[Batch]) -> str:
    """ 배치 객체가 들어있는 리스트에서 날짜 순으로 비교하여 할당 가능한 batch 객체에 라인 할당 후
    관련 id 리턴

    Args:
        line (OrderLine): 주문 라인
        batches (list[Batch]): 배치 객체가 들어있는 리스트

    Returns:
        str: batch.id
    """
    # next, iter 에 대해 궁금하다면 https://dojang.io/mod/page/view.php?id=2408
    try:
        batch = next(
            b for b in sorted(batches) if b.is_allocate(line)
        )
        batch.allocate(line)
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')
    return batch.id