import torch


class SparseAttention:
    def prepare(
        self, kv_full: torch.Tensor, num_blocks_to_select: int, block_size: int = 32
    ) -> torch.Tensor:
        pass

    def search(self, kv_repre: torch.Tensor, q: torch.Tensor) -> torch.Tensor:
        pass
