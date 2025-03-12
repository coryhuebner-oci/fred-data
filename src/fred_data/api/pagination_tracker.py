from dataclasses import dataclass


@dataclass
class PaginationTracker:
    current_offset: int
    expected_item_count: int

    @property
    def more_pages_to_read(self) -> bool:
        return self.current_offset < self.expected_item_count
