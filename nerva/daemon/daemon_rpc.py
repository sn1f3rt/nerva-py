from __future__ import annotations

from typing import Any, Optional, cast

import httpx

__all__ = ["DaemonRPC"]


class DaemonRPC:
    """
    A class to interact with the Nerva daemon's JSON-RPC interface.

    Parameters
    ----------
    host : str, optional
        The host of the daemon.
    port : int, optional
        The port of the daemon.
    ssl : bool, optional
        Whether to use SSL.
    timeout : float, optional
        The timeout for the request.

    Attributes
    ----------
    url : str
        The URL of the daemon.
    timeout : float
        The timeout for the request.
    headers : dict[str, str]
        The headers for the request.
    """

    __slots__ = ["url", "timeout", "headers", "auth"]

    def __init__(
        self,
        *,
        host: Optional[str] = "localhost",
        port: Optional[int] = 17566,
        ssl: Optional[bool] = False,
        timeout: Optional[float] = 10.0,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        self.url: str = f"{'https' if ssl else 'http'}://{host}:{port}"
        self.timeout: Optional[float] = timeout
        self.headers: dict[str, str] = {"Content-Type": "application/json"}
        self.auth: Optional[httpx.DigestAuth] = (
            httpx.DigestAuth(username, password) if username and password else None
        )

    async def _request(
        self, *, method: str, params: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Send a JSON-RPC request to the daemon.

        Parameters
        ----------
        method : str
            The JSON-RPC method name.
        params : dict[str, Any]
            The parameters for the method.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        async with httpx.AsyncClient(auth=self.auth) as client:
            response = await client.post(
                f"{self.url}/json_rpc",
                json={"jsonrpc": "2.0", "id": 0, "method": method, "params": params},
                headers=self.headers,
                timeout=self.timeout,
            )
            return cast(dict[str, Any], response.json())

    async def get_block_count(self) -> dict[str, Any]:
        """
        Get the current block count.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.
        """
        return await self._request(method="get_block_count", params={})

    async def on_get_block_hash(self, *, height: int) -> dict[str, Any]:
        """
        Get the block hash at a certain height.

        Parameters
        ----------
        height : int
            The height of the block.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            method="on_get_block_hash", params={"height": height}
        )

    async def get_block_template(
        self, *, wallet_address: str, reserve_size: int
    ) -> dict[str, Any]:
        """
        Get a block template for mining.

        Parameters
        ----------
        wallet_address : str
            The wallet address to mine to.

        reserve_size : int
            The reserve size.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            method="get_block_template",
            params={"wallet_address": wallet_address, "reserve_size": reserve_size},
        )

    async def submit_block(self, *, block_blob: list[str]) -> dict[str, Any]:
        """
        Submit a block to the network.

        Parameters
        ----------
        block_blob : list[str]
            The block blob to submit.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            method="submit_block", params={"blob": block_blob}
        )

    async def get_last_block_header(self) -> dict[str, Any]:
        """
        Get the last block header.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="get_last_block_header", params={})

    async def get_block_header_by_hash(self, *, block_hash: str) -> dict[str, Any]:
        """
        Get the block header by hash.

        Parameters
        ----------
        block_hash : str
            The hash of the block.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            method="get_block_header_by_hash", params={"hash": block_hash}
        )

    async def get_block_header_by_height(self, *, height: int) -> dict[str, Any]:
        """
        Get the block header by height.

        Parameters
        ----------
        height : int
            The height of the block.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            method="get_block_header_by_height", params={"height": height}
        )

    async def get_block_headers_range(
        self, *, start_height: int, end_height: int
    ) -> dict[str, Any]:
        """
        Get a range of block headers.

        Parameters
        ----------
        start_height : int
            The start height.
        end_height : int
            The end height.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            method="get_block_headers_range",
            params={"start_height": start_height, "end_height": end_height},
        )

    async def get_block(
        self, *, block_hash: Optional[str] = None, height: Optional[int] = None
    ) -> dict[str, Any]:
        """
        Get a block by hash or height.

        Parameters
        ----------
        block_hash : str, optional
            The hash of the block.
        height : int, optional
            The height of the block.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        if block_hash and not height:
            return await self._request(
                method="get_block", params={"hash": block_hash}
            )

        elif height and not block_hash:
            return await self._request(method="get_block", params={"height": height})

        else:
            raise ValueError("Either block_hash OR height must be provided.")

    async def get_connections(self) -> dict[str, Any]:
        """
        Get the connections to the daemon.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="get_connections", params={})

    async def get_info(self) -> dict[str, Any]:
        """
        Get the information about the daemon.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="get_info", params={})

    async def hard_fork_info(self) -> dict[str, Any]:
        """
        Get the hard fork information.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="hard_fork_info", params={})

    async def set_bans(self, *, bans: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Set bans for the daemon.

        Parameters
        ----------
        bans : list[dict[str, Any]]
            The bans to set. Each ban should be a dictionary with the following keys:
                - host : str
                    Host to ban (IP in A.B.C.D format).
                - ip : int, optional
                    IP to ban (int format).
                - ban : bool
                    Set `true` to ban, `false` to unban.
                - seconds : int
                    Time to ban in seconds.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="set_bans", params={"bans": bans})

    async def get_bans(self) -> dict[str, Any]:
        """
        Get the bans of the daemon.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="get_bans", params={})

    async def flush_txpool(
        self, *, txids: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """
        Flush the transaction pool.

        Parameters
        ----------
        txids : list, optional
            The transaction IDs to flush. If not provided, all transactions will be flushed.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            method="flush_txpool", params={"txids": txids or []}
        )

    async def get_output_histogram(
        self,
        *,
        amounts: list[int],
        min_count: int,
        max_count: int,
        unlocked: bool,
        recent_cutoff: int,
    ) -> dict[str, Any]:
        """
        Get the output histogram.

        Parameters
        ----------
        amounts : list
            The amounts to get the histogram for.
        min_count : int
            The minimum count.
        max_count : int
            The maximum count.
        unlocked : bool
            Whether to get the unlocked outputs.
        recent_cutoff : int
            The recent cutoff.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            method="get_output_histogram",
            params={
                "amounts": amounts,
                "min_count": min_count,
                "max_count": max_count,
                "unlocked": unlocked,
                "recent_cutoff": recent_cutoff,
            },
        )

    async def get_version(self) -> dict[str, Any]:
        """
        Get the version of the daemon.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="get_version", params={})

    async def get_coinbase_tx_sum(
        self, *, height: int, count: int
    ) -> dict[str, Any]:
        """
        Get the coinbase transaction sum.

        Parameters
        ----------
        height : int
            The height of the block.
        count : int
            The count of blocks.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            method="get_coinbase_tx_sum", params={"height": height, "count": count}
        )

    async def get_fee_estimate(
        self, *, grace_blocks: Optional[int] = None
    ) -> dict[str, Any]:
        """
        Get the fee estimate.

        Parameters
        ----------
        grace_blocks : int, optional
            The number of grace blocks.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            method="get_fee_estimate",
            params={"grace_blocks": grace_blocks} if grace_blocks else {},
        )

    async def get_alternate_chains(self) -> dict[str, Any]:
        """
        Get the alternate chains.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="get_alternate_chains", params={})

    async def relay_tx(self, *, txids: list[str]) -> dict[str, Any]:
        """
        Relay transactions to the network.

        Parameters
        ----------
        txids : list
            The transaction IDs to relay.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="relay_tx", params={"txids": txids})

    async def sync_info(self) -> dict[str, Any]:
        """
        Get the sync information of the daemon.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="sync_info", params={})

    async def get_txpool_backlog(self) -> dict[str, Any]:
        """
        Get the transaction pool backlog.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="get_txpool_backlog", params={})

    async def get_output_distribution(
        self,
        *,
        amounts: list[int],
        from_height: Optional[int] = 0,
        to_height: Optional[int] = 0,
        cumulative: Optional[bool] = False,
        binary: Optional[bool] = True,
        compress: Optional[bool] = False,
    ) -> dict[str, Any]:
        """
        Get the output distribution.

        Parameters
        ----------
        amounts : list[int]
            The amounts to get the distribution for.
        from_height : int, optional
            The height to start from.
        to_height : int, optional
            The height to end at.
        cumulative : bool, optional
            Whether to get the cumulative distribution.
        binary : bool, optional
            Whether to get the binary distribution.
        compress : bool, optional
            Whether to compress the distribution.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            method="get_output_distribution",
            params={
                "amounts": amounts,
                "from_height": from_height,
                "to_height": to_height,
                "cumulative": cumulative,
                "binary": binary,
                "compress": compress,
            },
        )

    async def prune_blockchain(self) -> dict[str, Any]:
        """
        Prune the blockchain.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="prune_blockchain", params={})

    async def flush_cache(
        self, *, bad_txs: Optional[bool] = False
    ) -> dict[str, Any]:
        """
        Flush the cache.

        Parameters
        ----------
        bad_txs : bool, optional
            Whether to flush the bad transactions.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="flush_cache", params={"bad_txs": bad_txs})

    async def get_generated_coins(
        self, *, height: Optional[int] = None
    ) -> dict[str, Any]:
        """
        Get the generated coins.

        Parameters
        ----------
        height : int, optional
            The height.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            method="get_generated_coins", params={"height": height} if height else {}
        )

    async def get_min_version(self) -> dict[str, Any]:
        """
        Get the minimum version of the daemon.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="get_min_version", params={})

    async def get_tx_pubkey(self, *, extra: str) -> dict[str, Any]:
        """
        Get the transaction public key.

        Parameters
        ----------
        extra : str
            The extra data.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="get_tx_pubkey", params={"extra": extra})

    async def decode_outputs(
        self, *, tx_hashes: list[str], sec_view_key: str, address: str
    ) -> dict[str, Any]:
        """
        Decode the outputs of transactions.

        Parameters
        ----------
        tx_hashes : list
            The transaction hashes.
        sec_view_key : str
            The secret view key.
        address : str
            The address to decode.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            method="decode_outputs",
            params={
                "tx_hashes": tx_hashes,
                "sec_view_key": sec_view_key,
                "address": address,
            },
        )

    async def add_peer(self, *, host: str) -> dict[str, Any]:
        """
        Add a peer to the daemon.

        Parameters
        ----------
        host : str
            The host of the peer.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(method="add_peer", params={"host": host})
