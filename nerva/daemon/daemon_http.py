from __future__ import annotations

from typing import Any, Optional, cast

import httpx

__all__ = ["DaemonHTTP"]


class DaemonHTTP:
    """
    A class to interact with the Nerva daemon's HTTP endpoint interface.

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
        self.url = f"{'https' if ssl else 'http'}://{host}:{port}"
        self.timeout = timeout
        self.headers = {"Content-Type": "application/json"}
        self.auth = (
            httpx.DigestAuth(username, password) if username and password else None
        )

    async def _request(
        self, *, endpoint: str, params: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Send an HTTP POST request to the daemon.

        Parameters
        ----------
        endpoint : str
            The HTTP endpoint path.
        params : dict[str, Any]
            The request body parameters.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        async with httpx.AsyncClient(auth=self.auth) as client:
            response = await client.post(
                f"{self.url}/{endpoint}",
                json=params,
                headers=self.headers,
                timeout=self.timeout,
            )
            return cast(dict[str, Any], response.json())

    async def get_height(self) -> dict[str, Any]:
        """
        Get the current block height.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="get_height", params={})

    async def get_blocks_bin(
        self, *, block_ids: list[str], start_height: int, prune: bool
    ) -> dict[str, Any]:
        """
        Get a list of blocks.

        Parameters
        ----------
        block_ids : list[str]
            Binary list of block IDs.
        start_height : int
            The start height.
        prune : bool
            Whether to prune the blocks.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="get_blocks.bin",
            params={
                "block_ids": block_ids,
                "start_height": start_height,
                "prune": prune,
            },
        )

    async def get_blocks_by_height_bin(
        self, *, heights: list[int]
    ) -> dict[str, Any]:
        """
        Get a list of blocks by height.

        Parameters
        ----------
        heights : list[int]
            The block heights to get.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="get_blocks_by_height.bin", params={"heights": heights}
        )

    async def get_hashes_bin(
        self, *, block_ids: list[str], start_height: int
    ) -> dict[str, Any]:
        """
        Get the hashes of blocks.

        Parameters
        ----------
        block_ids : list[str]
            Binary list of block IDs.
        start_height : int
            The start height.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="get_hashes.bin",
            params={"block_ids": block_ids, "start_height": start_height},
        )

    async def get_o_indexes_bin(self, *, txid: str) -> dict[str, Any]:
        """
        Get the output indexes of a transaction.

        Parameters
        ----------
        txid : str
            Binary transaction ID.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="get_o_indexes.bin", params={"txid": txid}
        )

    async def get_outs_bin(self, *, outputs: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Get the outputs.

        Parameters
        ----------
        outputs : list[dict[str, Any]]
            List of outputs as dictionaries with the following keys:
                - amount : int
                    The amount.
                - index : int
                    The index.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="get_outs.bin", params={"outputs": outputs}
        )

    async def get_transactions(
        self,
        *,
        txs_hashes: list[str],
        decode_as_json: Optional[bool] = False,
        prune: Optional[bool] = False,
        split: Optional[bool] = False,
    ) -> dict[str, Any]:
        """
        Get a list of transactions.

        Parameters
        ----------
        txs_hashes : list[str]
            List of transaction hashes.
        decode_as_json : bool, optional
            Whether to decode as JSON.
        prune : bool, optional
            Whether to prune the transactions.
        split : bool, optional
            Whether to split the transactions.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="get_transactions",
            params={
                "txs_hashes": txs_hashes,
                "decode_as_json": decode_as_json,
                "prune": prune,
                "split": split,
            },
        )

    async def get_alt_blocks_hashes(self) -> dict[str, Any]:
        """
        Get the hashes of alternate blocks.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="get_alt_blocks_hashes", params={})

    async def is_key_image_spent(self, *, key_images: list[str]) -> dict[str, Any]:
        """
        Check if key images are spent.

        Parameters
        ----------
        key_images : list[str]
            List of key images.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="is_key_image_spent", params={"key_images": key_images}
        )

    async def send_raw_transaction(
        self, *, tx_as_hex: str, do_not_relay: Optional[bool] = False
    ) -> dict[str, Any]:
        """
        Send a raw transaction.

        Parameters
        ----------
        tx_as_hex : str
            The transaction as hex.
        do_not_relay : bool, optional
            Whether to relay the transaction.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="send_raw_transaction",
            params={"tx_as_hex": tx_as_hex, "do_not_relay": do_not_relay},
        )

    async def start_mining(
        self,
        *,
        address: str,
        threads_count: int,
        do_background_mining: bool,
        ignore_battery: bool,
    ) -> dict[str, Any]:
        """
        Start mining.

        Parameters
        ----------
        address : str
            The address to mine to.
        threads_count : int
            The number of threads.
        do_background_mining : bool
            Whether to mine in the background.
        ignore_battery : bool
            Whether to ignore the battery.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="start_mining",
            params={
                "address": address,
                "threads_count": threads_count,
                "do_background_mining": do_background_mining,
                "ignore_battery": ignore_battery,
            },
        )

    async def set_donate_level(self, *, blocks: int) -> dict[str, Any]:
        """
        Set the donate level.

        Parameters
        ----------
        blocks : int
            The number of blocks to donate.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="set_donate_level", params={"blocks": blocks}
        )

    async def stop_mining(self) -> dict[str, Any]:
        """
        Stop mining.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="stop_mining", params={})

    async def mining_status(self) -> dict[str, Any]:
        """
        Get the mining status.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="mining_status", params={})

    async def save_bc(self) -> dict[str, Any]:
        """
        Save the blockchain.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="save_bc", params={})

    async def get_peer_list(self) -> dict[str, Any]:
        """
        Get the peer list.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="get_peer_list", params={})

    async def get_public_nodes(self) -> dict[str, Any]:
        """
        Get the public nodes.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="get_public_nodes", params={})

    async def set_log_hash_rate(self, *, visible: bool) -> dict[str, Any]:
        """
        Set the log hash rate.

        Parameters
        ----------
        visible : bool
            Whether to make the hash rate visible.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="set_log_hash_rate", params={"visible": visible}
        )

    async def set_log_level(self, *, level: int) -> dict[str, Any]:
        """
        Set the log level.

        Parameters
        ----------
        level : int
            The log level.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="set_log_level", params={"level": level})

    async def set_log_categories(self, *, categories: str) -> dict[str, Any]:
        """
        Set the log categories.

        Parameters
        ----------
        categories : str
            The log categories.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="set_log_categories", params={"categories": categories}
        )

    async def get_transaction_pool(self) -> dict[str, Any]:
        """
        Get the transaction pool.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="get_transaction_pool", params={})

    async def get_transaction_pool_hashes_bin(self) -> dict[str, Any]:
        """
        Get the transaction pool hashes.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="get_transaction_pool_hashes.bin", params={}
        )

    async def get_transaction_pool_hashes(self) -> dict[str, Any]:
        """
        Get the transaction pool hashes.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="get_transaction_pool_hashes", params={})

    async def get_transaction_pool_stats(self) -> dict[str, Any]:
        """
        Get the transaction pool stats.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="get_transaction_pool_stats", params={})

    async def set_bootstrap_daemon(
        self, *, address: str, username: str, password: str
    ) -> dict[str, Any]:
        """
        Set the bootstrap daemon.

        Parameters
        ----------
        address : str
            The address of the daemon.
        username : str
            The username.
        password : str
            The password.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="set_bootstrap_daemon",
            params={"address": address, "username": username, "password": password},
        )

    async def stop_daemon(self) -> dict[str, Any]:
        """
        Stop the daemon.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="stop_daemon", params={})

    async def get_info(self) -> dict[str, Any]:
        """
        Get the information of the daemon.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="get_info", params={})

    async def get_net_stats(self) -> dict[str, Any]:
        """
        Get the network stats.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="get_net_stats", params={})

    async def get_limit(self) -> dict[str, Any]:
        """
        Get daemon bandwidth limits.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="get_limit", params={})

    async def set_limit(self, *, limit_down: int, limit_up: int) -> dict[str, Any]:
        """
        Set daemon bandwidth limits.

        Parameters
        ----------
        limit_down : int
            The download limit. (-1 to change to default; 0 for no change)
        limit_up : int
            The upload limit. (-1 to change to default; 0 for no change)

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="set_limit",
            params={"limit_down": limit_down, "limit_up": limit_up},
        )

    async def out_peers(self) -> dict[str, Any]:
        """
        Get the outgoing peers.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="out_peers", params={})

    async def in_peers(self) -> dict[str, Any]:
        """
        Get the incoming peers.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="in_peers", params={})

    async def get_outs(
        self, *, outputs: list[dict[str, Any]], get_txid: bool
    ) -> dict[str, Any]:
        """
        Get outputs.

        Parameters
        ----------
        outputs : list[dict[str, Any]]
            List of outputs as dictionaries with the following keys:
                - amount : int
                    The amount.
                - index : int
                    The index.
        get_txid : bool
            Whether to get the transaction ID.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="get_outs", params={"outputs": outputs, "get_txid": get_txid}
        )

    async def update(self) -> dict[str, Any]:
        """
        Update the daemon.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(endpoint="update", params={})

    async def get_output_distribution_bin(
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
            endpoint="get_output_distribution.bin",
            params={
                "amounts": amounts,
                "from_height": from_height,
                "to_height": to_height,
                "cumulative": cumulative,
                "binary": binary,
                "compress": compress,
            },
        )

    async def pop_blocks(self, *, nblocks: int) -> dict[str, Any]:
        """
        Pop blocks from the blockchain.

        Parameters
        ----------
        nblocks : int
            The number of blocks to pop.

        Returns
        -------
        dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            endpoint="pop_blocks", params={"nblocks": nblocks}
        )
