from __future__ import annotations

from typing import Any, Optional, cast

import httpx

__all__ = ["WalletRPC"]


class WalletRPC:
    """
    A class to interact with the Nerva wallet's JSON-RPC interface.

    Parameters
    ----------
    port : int
        The port of the wallet's JSON-RPC interface.
    host : str, optional
        The host of the wallet's JSON-RPC interface. Default is "localhost".
    ssl : bool, optional
        Whether to use SSL. Default is False.
    timeout : float, optional
        The timeout for the request. Default is 10.0.
    username : str, optional
        The username for the wallet's JSON-RPC interface. Default is "".
    password : str, optional
        The password for the wallet's JSON-RPC interface. Default is "".

    Attributes
    ----------
    url : str
        The URL of the wallet's JSON-RPC interface.
    auth : httpx.DigestAuth | None
        The authentication for the wallet's JSON-RPC interface.
    timeout : float
        The timeout for the request.
    headers : dict[str, str]
        The headers for the request.

    """

    __slots__ = [
        "url",
        "auth",
        "timeout",
        "headers",
    ]

    def __init__(
        self,
        *,
        port: int,
        host: str = "localhost",
        ssl: bool = False,
        timeout: float = 10.0,
        username: str = "",
        password: str = "",
    ) -> None:
        self.url: str = f"http{'s' if ssl else ''}://{host}:{port}"
        self.timeout: float = timeout
        self.headers: dict[str, str] = {"Content-Type": "application/json"}
        self.auth: Optional[httpx.DigestAuth] = (
            httpx.DigestAuth(username, password) if username and password else None
        )

    async def _request(
        self, *, method: str, params: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Send a JSON-RPC request to the wallet.

        Parameters
        ----------
        method : str
            The JSON-RPC method name.
        params : dict[str, Any]
            The parameters for the method.

        Returns
        -------
        dict[str, Any]
            The response from the wallet.

        """
        async with httpx.AsyncClient(auth=self.auth) as client:
            response = await client.post(
                f"{self.url}/json_rpc",
                json={"jsonrpc": "2.0", "id": 0, "method": method, "params": params},
                headers=self.headers,
                timeout=self.timeout,
            )
            return cast(dict[str, Any], response.json())

    async def get_balance(
        self, *, account_index: int, address_indices: Optional[list[int]] = None
    ) -> dict[str, Any]:
        """
        Return the wallet's balance.

        Parameters
        ----------
        account_index : int
            Return balance for this account.
        address_indices : list[int], optional
            Return balance detail for those subaddresses.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.
        """
        return await self._request(
            method="get_balance",
            params={
                "account_index": account_index,
                "address_indices": address_indices or [],
            },
        )

    async def get_address(
        self, *, account_index: int, address_indices: Optional[list[int]] = None
    ) -> dict[str, Any]:
        """
        Return the wallet's addresses for an account. Optionally filter for specific set of subaddresses.

        Parameters
        ----------
        account_index : int
            Get addresses for this account.
        address_indices : list[int], optional
            Return specific set of subaddresses.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="get_address",
            params={
                "account_index": account_index,
                "address_indices": address_indices or [],
            },
        )

    async def get_address_index(self, *, address: str) -> dict[str, Any]:
        """
        Get account and address indexes from a specific (sub)address.

        Parameters
        ----------
        address : str
            The (sub)address to look for.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="get_address_index", params={"address": address}
        )

    async def create_address(
        self, *, account_index: int, label: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Create a new address for an account.

        Parameters
        ----------
        account_index : int
            Create a new address for this account.
        label : str, optional
            Label for the new address.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="create_address",
            params={"account_index": account_index, "label": label},
        )

    async def label_address(
        self, *, index: dict[str, int], label: str
    ) -> dict[str, Any]:
        """
        Label an address.

        Parameters
        ----------
        index : dict[str, int]
            Subaddress index in the form {"major": 0, "minor": 0}.
        label : str
            The label of the address.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="label_address", params={"index": index, "label": label}
        )

    async def get_accounts(self, *, tag: Optional[str] = None) -> dict[str, Any]:
        """
        Return the wallet's accounts.

        Parameters
        ----------
        tag : str, optional
            Tag for filtering accounts.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="get_accounts", params={"tag": tag})

    async def create_account(self, *, label: Optional[str] = None) -> dict[str, Any]:
        """
        Create a new account.

        Parameters
        ----------
        label : str, optional
            The label of the account.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="create_account", params={"label": label})

    async def label_account(
        self, *, account_index: int, label: str
    ) -> dict[str, Any]:
        """
        Label an account.

        Parameters
        ----------
        account_index : int
            The index of the account.
        label : str
            The label of the account.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="label_account",
            params={"account_index": account_index, "label": label},
        )

    async def get_account_tags(self) -> dict[str, Any]:
        """
        Return the wallet's account tags.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="get_account_tags", params={})

    async def tag_accounts(self, *, tag: str, accounts: list[int]) -> dict[str, Any]:
        """
        Apply a filtering tag to a list of accounts.

        Parameters
        ----------
        tag : str
            The tag to apply.
        accounts : list[int]
            The accounts to tag.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="tag_accounts", params={"tag": tag, "accounts": accounts}
        )

    async def untag_accounts(self, *, accounts: list[int]) -> dict[str, Any]:
        """
        Remove filtering tag from a list of accounts.

        Parameters
        ----------
        accounts : list[int]
            The accounts to untag.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="untag_accounts", params={"accounts": accounts}
        )

    async def set_account_tag_description(
        self, *, tag: str, description: str
    ) -> dict[str, Any]:
        """
        Set description for an account tag.

        Parameters
        ----------
        tag : str
            The tag to set description for.
        description : str
            Description for the tag.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.
        """
        return await self._request(
            method="set_account_tag_description",
            params={"tag": tag, "description": description},
        )

    async def get_height(self) -> dict[str, Any]:
        """
        Return the wallet's current block height.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="get_height", params={})

    async def transfer(
        self,
        *,
        destinations: list[dict[str, Any]],
        account_index: int,
        subaddr_indices: list[int],
        priority: int,
        mixin: int,
        ring_size: int,
        unlock_time: int,
        get_tx_key: bool,
        get_tx_hex: bool,
        get_tx_metadata: bool,
        do_not_relay: bool,
        payment_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Send a transfer from the wallet to a single recipient.

        Parameters
        ----------
        destinations : list[dict[str, Any]]
            The destinations to send the transfer to.
        account_index : int
            The account to send the transfer from.
        subaddr_indices : list[int]
            Array of subaddress indices to send from.
        priority : int
            Set a priority for the transfer.
        mixin : int
            Number of outputs from the blockchain to mix with (0 means no mixing).
        ring_size : int
            Sets ringsize for each transaction.
        unlock_time : int
            Number of blocks before the Nerva can be spent (0 to not add a lock).
        get_tx_key : bool
            Return the transaction key after sending.
        get_tx_hex : bool
            Return the transaction as hex string after sending.
        get_tx_metadata : bool
            Return the transaction metadata.
        do_not_relay : bool
            If true, the transfer won't be relayed to the Nerva network.
        payment_id : str, optional
            Random 32-byte/64-character hex string to identify a transaction.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="transfer",
            params={
                "destinations": destinations,
                "account_index": account_index,
                "subaddr_indices": subaddr_indices,
                "priority": priority,
                "mixin": mixin,
                "ring_size": ring_size,
                "unlock_time": unlock_time,
                "get_tx_key": get_tx_key,
                "get_tx_hex": get_tx_hex,
                "get_tx_metadata": get_tx_metadata,
                "do_not_relay": do_not_relay,
                "payment_id": payment_id,
            },
        )

    async def transfer_split(
        self,
        *,
        destinations: list[dict[str, Any]],
        account_index: int,
        subaddr_indices: list[int],
        priority: int,
        mixin: int,
        ring_size: int,
        unlock_time: int,
        get_tx_keys: bool,
        get_tx_hex: bool,
        get_tx_metadata: bool,
        do_not_relay: bool,
        payment_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Send a transfer from the wallet to multiple recipients.

        Parameters
        ----------
        destinations : list[dict[str, Any]]
            The destinations to send the transfer to.
        account_index : int
            The account to send the transfer from.
        subaddr_indices : list[int]
            Array of subaddress indices to send from.
        priority : int
            Set a priority for the transfer.
        mixin : int
            Number of outputs from the blockchain to mix with (0 means no mixing).
        ring_size : int
            Sets ringsize for each transaction.
        unlock_time : int
            Number of blocks before the Nerva can be spent (0 to not add a lock).
        get_tx_keys : bool
            Return the transaction keys after sending.
        get_tx_hex : bool
            Return the transaction as hex string after sending.
        get_tx_metadata : bool
            Return the transaction metadata.
        do_not_relay : bool
            If true, the transfer won't be relayed to the Nerva network.
        payment_id : str, optional
            Random 32-byte/64-character hex string to identify a transaction.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="transfer_split",
            params={
                "destinations": destinations,
                "account_index": account_index,
                "subaddr_indices": subaddr_indices,
                "priority": priority,
                "mixin": mixin,
                "ring_size": ring_size,
                "unlock_time": unlock_time,
                "get_tx_keys": get_tx_keys,
                "get_tx_hex": get_tx_hex,
                "get_tx_metadata": get_tx_metadata,
                "do_not_relay": do_not_relay,
                "payment_id": payment_id,
            },
        )

    async def sign_transfer(
        self, *, unsigned_txset: str, export_raw: Optional[bool] = False
    ) -> dict[str, Any]:
        """
        Sign a transaction created on a read-only wallet (in cold-signing process).

        Parameters
        ----------
        unsigned_txset : str
            Set of unsigned tx returned by "transfer" method.
        export_raw : bool, optional
            If true, return the raw transaction data. Default is False.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="sign_transfer",
            params={"unsigned_txset": unsigned_txset, "export_raw": export_raw},
        )

    async def describe_transfer(self, *, unsigned_txset: str) -> dict[str, Any]:
        """
        Return a list of unsigned transfers in the set, their count, and total amount.

        Parameters
        ----------
        unsigned_txset : str
            Set of unsigned tx returned by "transfer" method.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="describe_transfer", params={"unsigned_txset": unsigned_txset}
        )

    async def submit_transfer(self, *, tx_data_hex: str) -> dict[str, Any]:
        """
        Submit a previously signed transaction.

        Parameters
        ----------
        tx_data_hex : str
            Transaction in hex format.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="submit_transfer", params={"tx_data_hex": tx_data_hex}
        )

    async def sweep_dust(
        self,
        *,
        get_tx_keys: Optional[bool] = False,
        do_not_relay: Optional[bool] = False,
        get_tx_hex: Optional[bool] = False,
        get_tx_metadata: Optional[bool] = False,
    ) -> dict[str, Any]:
        """
        Sweep the dust from the wallet.

        Parameters
        ----------
        get_tx_keys : bool, optional
            Return the transaction keys after sending.
        do_not_relay : bool, optional
            If true, do not relay this sweep transfer.
        get_tx_hex : bool, optional
            Return the transactions as hex string after sending.
        get_tx_metadata : bool, optional
            Return the transaction metadata.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="sweep_dust",
            params={
                "get_tx_keys": get_tx_keys,
                "do_not_relay": do_not_relay,
                "get_tx_hex": get_tx_hex,
                "get_tx_metadata": get_tx_metadata,
            },
        )

    async def sweep_unmixable(self) -> dict[str, Any]:
        """
        Sweep unmixable outputs from the wallet.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="sweep_unmixable", params={})

    async def sweep_all(
        self,
        *,
        address: str,
        account_index: int,
        subaddr_indices: list[int],
        priority: int,
        mixin: int,
        ring_size: int,
        unlock_time: int,
        get_tx_keys: bool,
        below_amount: int,
        do_not_relay: bool,
        get_tx_hex: bool,
        get_tx_metadata: bool,
        payment_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Sweep all unlocked outputs in a specified subaddress to an address.

        Parameters
        ----------
        address : str
            Destination public address.
        account_index : int
            Account to sweep from.
        subaddr_indices : list[int]
            Array of subaddress indices to sweep from.
        priority : int
            Set a priority for the transfer.
        mixin : int
            Number of outputs from the blockchain to mix with (0 means no mixing).
        ring_size : int
            Sets ringsize for each transaction.
        unlock_time : int
            Number of blocks before the Nerva can be spent (0 to not add a lock).
        get_tx_keys : bool
            Return the transaction keys after sending.
        below_amount : int
            Sweep all outputs below this amount.
        do_not_relay : bool
            If true, do not relay this sweep transfer.
        get_tx_hex : bool
            Return the transactions as hex string after sending.
        get_tx_metadata : bool
            Return the transaction metadata.
        payment_id : str, optional
            Random 32-byte/64-character hex string to identify a transaction.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="sweep_all",
            params={
                "address": address,
                "account_index": account_index,
                "subaddr_indices": subaddr_indices,
                "priority": priority,
                "mixin": mixin,
                "ring_size": ring_size,
                "unlock_time": unlock_time,
                "get_tx_keys": get_tx_keys,
                "below_amount": below_amount,
                "do_not_relay": do_not_relay,
                "get_tx_hex": get_tx_hex,
                "get_tx_metadata": get_tx_metadata,
                "payment_id": payment_id,
            },
        )

    async def sweep_single(
        self,
        *,
        address: str,
        priority: int,
        mixin: int,
        ring_size: int,
        unlock_time: int,
        get_tx_key: bool,
        get_tx_hex: bool,
        get_tx_metadata: bool,
        do_not_relay: bool,
        payment_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Sweep a single output to an address.

        Parameters
        ----------
        address : str
            Destination public address.
        priority : int
            Set a priority for the transfer.
        mixin : int
            Number of outputs from the blockchain to mix with (0 means no mixing).
        ring_size : int
            Sets ringsize for each transaction.
        unlock_time : int
            Number of blocks before the Nerva can be spent (0 to not add a lock).
        get_tx_key : bool
            Return the transaction keys after sending.
        get_tx_hex : bool
            Return the transaction as hex string after sending.
        get_tx_metadata : bool
            Return the transaction metadata.
        do_not_relay : bool
            If true, the transfer won't be relayed to the Nerva network.
        payment_id : str, optional
            Random 32-byte/64-character hex string to identify a transaction.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="sweep_single",
            params={
                "address": address,
                "priority": priority,
                "mixin": mixin,
                "ring_size": ring_size,
                "unlock_time": unlock_time,
                "get_tx_key": get_tx_key,
                "get_tx_hex": get_tx_hex,
                "get_tx_metadata": get_tx_metadata,
                "do_not_relay": do_not_relay,
                "payment_id": payment_id,
            },
        )

    async def relay_tx(self, *, tx_hex: str) -> dict[str, Any]:
        """
        Relay a transaction previously created with "do_not_relay" set to true.

        Parameters
        ----------
        tx_hex : str
            Transaction in hex format.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="relay_tx", params={"hex": tx_hex})

    async def store(self) -> dict[str, Any]:
        """
        Save the wallet file.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="store", params={})

    async def get_payments(self, *, payment_id: str) -> dict[str, Any]:
        """
        Return a list of incoming payments using a given payment ID.

        Parameters
        ----------
        payment_id : str
            Payment ID to query.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="get_payments", params={"payment_id": payment_id}
        )

    async def get_bulk_payments(
        self, *, payment_ids: list[str], min_block_height: int
    ) -> dict[str, Any]:
        """
        Return a list of incoming payments using a given payment ID.

        Parameters
        ----------
        payment_ids : list[str]
            Payment IDs to query.
        min_block_height : int
            The minimum block height to scan.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="get_bulk_payments",
            params={
                "payment_ids": payment_ids,
                "min_block_height": min_block_height,
            },
        )

    async def incoming_transfers(
        self,
        *,
        transfer_type: str,
        account_index: int,
        subaddr_indices: list[int],
        verbose: Optional[bool] = False,
    ) -> dict[str, Any]:
        """
        Return a list of incoming transfers to the wallet.

        Parameters
        ----------
        transfer_type : str
            "all": all the transfers.
            "available": only transfers which are not yet spent.
            "unavailable": only transfers which are already spent.
        account_index : int
            Return transfers for this account.
        subaddr_indices : list[int]
            Array of subaddress indices to query.
        verbose : bool, optional
            Enable verbose output.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="incoming_transfers",
            params={
                "transfer_type": transfer_type,
                "account_index": account_index,
                "subaddr_indices": subaddr_indices,
                "verbose": verbose,
            },
        )

    async def query_key(self, *, key_type: str) -> dict[str, Any]:
        """
        Return the spend or view private key.

        Parameters
        ----------
        key_type : str
            "mnemonic": the mnemonic seed.
            "view_key": the view key.
            "spend_key": the spend key.
            "seed": the mnemonic seed.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="query_key", params={"key_type": key_type})

    async def make_integrated_address(
        self, *, payment_id: str, standard_address: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Make an integrated address from the wallet address and a payment ID.

        Parameters
        ----------
        payment_id : str
            Payment ID.
        standard_address : str, optional
            Destination public address. If not provided, the wallet's address is used.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="make_integrated_address",
            params={"payment_id": payment_id, "standard_address": standard_address},
        )

    async def split_integrated_address(
        self, *, integrated_address: str
    ) -> dict[str, Any]:
        """
        Retrieve the standard address and payment ID corresponding to an integrated address.

        Parameters
        ----------
        integrated_address : str
            Integrated address to split.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="split_integrated_address",
            params={"integrated_address": integrated_address},
        )

    async def stop_wallet(self) -> dict[str, Any]:
        """
        Stop the wallet.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="stop_wallet", params={})

    async def rescan_blockchain(self) -> dict[str, Any]:
        """
        Re-scan the blockchain.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="rescan_blockchain", params={})

    async def set_tx_notes(
        self, *, txids: list[str], notes: list[str]
    ) -> dict[str, Any]:
        """
        Set arbitrary string notes for transactions.

        Parameters
        ----------
        txids : list[str]
            Array of transaction IDs.
        notes : list[str]
            Notes for the transactions.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="set_tx_notes", params={"txids": txids, "notes": notes}
        )

    async def get_tx_notes(self, *, txids: list[str]) -> dict[str, Any]:
        """
        Get string notes for transactions.

        Parameters
        ----------
        txids : list[str]
            Array of transaction IDs.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="get_tx_notes", params={"txids": txids})

    async def set_attribute(self, *, key: str, value: str) -> dict[str, Any]:
        """
        Set arbitrary attribute.

        Parameters
        ----------
        key : str
            Attribute name.
        value : str
            Attribute value.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="set_attribute", params={"key": key, "value": value}
        )

    async def get_attribute(self, *, key: str) -> dict[str, Any]:
        """
        Get an attribute.

        Parameters
        ----------
        key : str
            Attribute name.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="get_attribute", params={"key": key})

    async def get_tx_key(self, *, txid: str) -> dict[str, Any]:
        """
        Get transaction secret key.

        Parameters
        ----------
        txid : str
            Transaction ID.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="get_tx_key", params={"txid": txid})

    async def check_tx_key(
        self, *, txid: str, tx_key: str, address: str
    ) -> dict[str, Any]:
        """
        Check a transaction in the blockchain with its secret key.

        Parameters
        ----------
        txid : str
            Transaction ID.
        tx_key : str
            Transaction secret key.
        address : str
            Destination public address.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="check_tx_key",
            params={"txid": txid, "tx_key": tx_key, "address": address},
        )

    async def get_tx_proof(
        self, *, txid: str, address: str, message: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Generate a signature to prove a transaction in the blockchain.

        Parameters
        ----------
        txid : str
            Transaction ID.
        address : str
            Destination public address.
        message : str, optional
            Add a message to the signature to further authenticate.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="get_tx_proof",
            params={"txid": txid, "address": address, "message": message},
        )

    async def check_tx_proof(
        self,
        *,
        txid: str,
        address: str,
        signature: str,
        message: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Prove a transaction by checking its signature.

        Parameters
        ----------
        txid : str
            Transaction ID.
        address : str
            Destination public address.
        signature : str
            Transaction signature.
        message : str, optional
            Add a message to the signature to further authenticate.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="check_tx_proof",
            params={
                "txid": txid,
                "address": address,
                "signature": signature,
                "message": message,
            },
        )

    async def get_spend_proof(
        self, *, txid: str, message: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Generate a signature to prove a spend using the key of the transaction.

        Parameters
        ----------
        txid : str
            Transaction ID.
        message : str, optional
            Add a message to the signature to further authenticate.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="get_spend_proof", params={"txid": txid, "message": message}
        )

    async def check_spend_proof(
        self, *, txid: str, signature: str, message: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Prove a spend using the key of the transaction.

        Parameters
        ----------
        txid : str
            Transaction ID.
        signature : str
            Spend signature.
        message : str, optional
            Add a message to the signature to further authenticate.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="check_spend_proof",
            params={"txid": txid, "message": message, "signature": signature},
        )

    async def get_reserve_proof(
        self,
        *,
        all_reserve: bool,
        account_index: int,
        amount: int,
        message: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Generate a signature to prove of a reserve proof.

        Parameters
        ----------
        all_reserve : bool
            Proves all wallet reserve.
        account_index : int
            Account to prove reserve for.
        amount : int
            Amount to prove.
        message : str, optional
            Add a message to the signature to further authenticate.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="get_reserve_proof",
            params={
                "all": all_reserve,
                "account_index": account_index,
                "amount": amount,
                "message": message,
            },
        )

    async def check_reserve_proof(
        self, *, address: str, signature: str, message: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Prove a wallet has a disposable reserve using a signature.

        Parameters
        ----------
        address : str
            Public address.
        signature : str
            Reserve proof signature.
        message : str, optional
            Add a message to the signature to further authenticate.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="check_reserve_proof",
            params={"address": address, "message": message, "signature": signature},
        )

    async def get_transfers(
        self,
        *,
        incoming: Optional[bool] = False,
        outgoing: Optional[bool] = False,
        pending: Optional[bool] = False,
        failed: Optional[bool] = False,
        pool: Optional[bool] = False,
        filter_by_height: Optional[bool] = False,
        min_height: Optional[int] = None,
        max_height: Optional[int] = None,
        account_index: Optional[int] = None,
        subaddr_indices: Optional[list[int]] = None,
    ) -> dict[str, Any]:
        """
        Return a list of transfers.

        Parameters
        ----------
        incoming : bool, optional
            Include incoming transfers.
        outgoing : bool, optional
            Include outgoing transfers.
        pending : bool, optional
            Include pending transfers.
        failed : bool, optional
            Include failed transfers.
        pool : bool, optional
            Include transfers from the daemon's transaction pool.
        filter_by_height : bool, optional
            Filter transfers by block height.
        min_height : int, optional
            Minimum block height to scan for transfers.
        max_height : int, optional
            Maximum block height to scan for transfers.
        account_index : int, optional
            Return transfers for this account.
        subaddr_indices : list[int], optional
            Array of subaddress indices to query.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="get_transfers",
            params={
                "in": incoming,
                "out": outgoing,
                "pending": pending,
                "failed": failed,
                "pool": pool,
                "filter_by_height": filter_by_height,
                "min_height": min_height,
                "max_height": max_height,
                "account_index": account_index,
                "subaddr_indices": subaddr_indices or [],
            },
        )

    async def get_transfer_by_txid(
        self, *, txid: str, account_index: Optional[int] = None
    ) -> dict[str, Any]:
        """
        Return a list of transfers for the given txid.

        Parameters
        ----------
        txid : str
            Transaction ID.
        account_index : int, optional
            Return transfers for this account.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="get_transfer_by_txid",
            params={"txid": txid, "account_index": account_index},
        )

    async def sign(self, *, data: str) -> dict[str, Any]:
        """
        Sign a string.

        Parameters
        ----------
        data : str
            Data to sign.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="sign", params={"data": data})

    async def verify(
        self, *, data: str, address: str, signature: str
    ) -> dict[str, Any]:
        """
        Verify a signature on a string.

        Parameters
        ----------
        data : str
            Data to verify.
        address : str
            Public address.
        signature : str
            Signature to verify.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="verify",
            params={"data": data, "address": address, "signature": signature},
        )

    async def export_outputs(self) -> dict[str, Any]:
        """
        Export all outputs in hex format.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="export_outputs", params={})

    async def import_outputs(self, *, outputs_data_hex: str) -> dict[str, Any]:
        """
        Import outputs in hex format.

        Parameters
        ----------
        outputs_data_hex : str
            Outputs to import in hex format.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="import_outputs", params={"outputs_data_hex": outputs_data_hex}
        )

    async def export_key_images(self) -> dict[str, Any]:
        """
        Export a signed set of key images.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="export_key_images", params={})

    async def import_key_images(
        self, *, signed_key_images: list[str], key_image: str, signature: str
    ) -> dict[str, Any]:
        """
        Import signed key images list and verify their spent status.

        Parameters
        ----------
        signed_key_images : list[str]
            Array of signed key images in hex format.
        key_image : str
            Key image to import.
        signature : str
            Signature of the key image.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="import_key_images",
            params={
                "signed_key_images": signed_key_images,
                "key_image": key_image,
                "signature": signature,
            },
        )

    async def make_uri(
        self,
        *,
        address: str,
        amount: Optional[int] = None,
        payment_id: Optional[str] = None,
        recipient_name: Optional[str] = None,
        tx_description: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Create a payment URI using the official URI spec.

        Parameters
        ----------
        address : str
            Destination public address.
        amount : int, optional
            Amount to send.
        payment_id : str, optional
            Random 32-byte/64-character hex string to identify a transaction.
        recipient_name : str, optional
            Name of the payment recipient.
        tx_description : str, optional
            Description of the reason for the tx.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="make_uri",
            params={
                "address": address,
                "amount": amount,
                "payment_id": payment_id,
                "recipient_name": recipient_name,
                "tx_description": tx_description,
            },
        )

    async def parse_uri(self, *, uri: str) -> dict[str, Any]:
        """
        Parse a payment URI to get payment information.

        Parameters
        ----------
        uri : str
            Payment URI.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="parse_uri", params={"uri": uri})

    async def get_address_book(self, *, entries: list[int]) -> dict[str, Any]:
        """
        Return the wallet's address book.

        Parameters
        ----------
        entries : list[int]
            Array of address book entries.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="get_address_book", params={"entries": entries}
        )

    async def add_address_book(
        self,
        *,
        address: str,
        payment_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Add an entry to the wallet's address book.

        Parameters
        ----------
        address : str
            Destination public address.
        payment_id : str, optional
            Random 32-byte/64-character hex string to identify a transaction.
        description : str, optional
            Description of the address.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="add_address_book",
            params={
                "address": address,
                "payment_id": payment_id,
                "description": description,
            },
        )

    async def edit_address_book(
        self,
        *,
        index: int,
        set_address: Optional[bool] = False,
        address: Optional[str] = None,
        set_description: Optional[bool] = False,
        description: Optional[str] = None,
        set_payment_id: Optional[bool] = False,
        payment_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Edit an existing entry in the wallet's address book.

        Parameters
        ----------
        index : int
            The index of the address book entry to edit.
        set_address : bool, optional
            Set the address.
        address : str, optional
            Destination public address.
        set_description : bool, optional
            Set the description.
        description : str, optional
            Description of the address.
        set_payment_id : bool, optional
            Set the payment ID.
        payment_id : str, optional
            Random 32-byte/64-character hex string to identify a transaction.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="edit_address_book",
            params={
                "index": index,
                "set_address": set_address,
                "address": address,
                "set_description": set_description,
                "description": description,
                "set_payment_id": set_payment_id,
                "payment_id": payment_id,
            },
        )

    async def delete_address_book(self, *, index: int) -> dict[str, Any]:
        """
        Delete an entry from the wallet's address book.

        Parameters
        ----------
        index : int
            The index of the address book entry to delete.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="delete_address_book", params={"index": index}
        )

    async def refresh(self, *, start_height: Optional[int] = None) -> dict[str, Any]:
        """
        Refresh the wallet.

        Parameters
        ----------
        start_height : int, optional
            Start height to refresh from.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="refresh", params={"start_height": start_height}
        )

    async def auto_refresh(
        self, *, enable: Optional[bool] = True, period: Optional[int] = None
    ) -> dict[str, Any]:
        """
        Set whether to automatically refresh the wallet.

        Parameters
        ----------
        enable : bool
            Enable or disable auto refresh.
        period : int, optional
            Set the refresh period.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="auto_refresh", params={"enable": enable, "period": period}
        )

    async def rescan_spent(self) -> dict[str, Any]:
        """
        Re-scan spent outputs.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="rescan_spent", params={})

    async def start_mining(
        self, *, threads_count: int, do_background_mining: bool, ignore_battery: bool
    ) -> dict[str, Any]:
        """
        Start mining in the wallet.

        Parameters
        ----------
        threads_count : int
            Number of threads to use for mining.
        do_background_mining : bool
            If true, mine in the background.
        ignore_battery : bool
            If true, mine even if battery is low.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="start_mining",
            params={
                "threads_count": threads_count,
                "do_background_mining": do_background_mining,
                "ignore_battery": ignore_battery,
            },
        )

    async def set_donate_level(self, *, blocks: int) -> dict[str, Any]:
        """
        Set the donation level for the Nerva network.

        Parameters
        ----------
        blocks : int
            Number of blocks to donate.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="set_donate_level", params={"blocks": blocks}
        )

    async def stop_mining(self) -> dict[str, Any]:
        """
        Stop mining in the wallet.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="stop_mining", params={})

    async def get_languages(self) -> dict[str, Any]:
        """
        Return the list of available languages for the wallet's seed.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="get_languages", params={})

    async def create_wallet(
        self,
        *,
        filename: str,
        language: str,
        password: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Create a new wallet.

        Parameters
        ----------
        filename : str
            Wallet file name.
        language : str
            Language for seed.
        password : str, optional
            Wallet password.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="create_wallet",
            params={
                "filename": filename,
                "password": password or "",
                "language": language,
            },
        )

    async def create_hw_wallet(
        self, *, filename: str, language: str, device_name: str, restore_height: int
    ) -> dict[str, Any]:
        """
        Create a wallet from a hardware device.

        Parameters
        ----------
        filename : str
            Wallet file name.
        language : str
            Wallet language.
        device_name : str
            Hardware device name.
        restore_height : int
            Wallet restore height.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="create_hw_wallet",
            params={
                "filename": filename,
                "language": language,
                "device_name": device_name,
                "restore_height": restore_height,
            },
        )

    async def open_wallet(
        self, *, filename: str, password: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Open a wallet.

        Parameters
        ----------
        filename : str
            Wallet file name.
        password : str, optional
            Wallet password.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="open_wallet",
            params={"filename": filename, "password": password or ""},
        )

    async def close_wallet(self) -> dict[str, Any]:
        """
        Close the wallet.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="close_wallet", params={})

    async def change_wallet_password(
        self,
        *,
        old_password: Optional[str] = None,
        new_password: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Change the wallet password.

        Parameters
        ----------
        old_password : str, optional
            Old wallet password.
        new_password : str, optional
            New wallet password.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="change_wallet_password",
            params={
                "old_password": old_password or "",
                "new_password": new_password or "",
            },
        )

    async def restore_wallet_from_seed(
        self, *, filename: str, seed: str, restore_height: int
    ) -> dict[str, Any]:
        """
        Restore a wallet from a mnemonic seed.

        Parameters
        ----------
        filename : str
            Wallet file name.
        seed : str
            Wallet mnemonic seed.
        restore_height : int
            Wallet restore height.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="restore_wallet_from_seed",
            params={
                "filename": filename,
                "seed": seed,
                "restore_height": restore_height,
            },
        )

    async def restore_wallet_from_keys(
        self,
        *,
        filename: str,
        address: str,
        viewkey: str,
        spendkey: str,
        restore_height: int,
    ) -> dict[str, Any]:
        """
        Restore a wallet from a set of keys.

        Parameters
        ----------
        filename : str
            Wallet file name.
        address : str
            Wallet public address.
        viewkey : str
            Wallet view key.
        spendkey : str
            Wallet spend key.
        restore_height : int
            Wallet restore height.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="restore_wallet_from_keys",
            params={
                "filename": filename,
                "address": address,
                "viewkey": viewkey,
                "spendkey": spendkey,
                "restore_height": restore_height,
            },
        )

    async def is_multisig(self) -> dict[str, Any]:
        """
        Check if the wallet is a multisig wallet.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="is_multisig", params={})

    async def prepare_multisig(self) -> dict[str, Any]:
        """
        Prepare a wallet for multisig use.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="prepare_multisig", params={})

    async def make_multisig(
        self, *, multisig_info: list[str], threshold: int, password: str
    ) -> dict[str, Any]:
        """
        Make a wallet multisig.

        Parameters
        ----------
        multisig_info : list[str]
            Array of multisig info from other participants.
        threshold : int
            Number of signatures needed to sign a transfer.
        password : str
            Wallet password.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="make_multisig",
            params={
                "multisig_info": multisig_info,
                "threshold": threshold,
                "password": password,
            },
        )

    async def export_multisig_info(self) -> dict[str, Any]:
        """
        Export multisig info for other participants.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="export_multisig_info", params={})

    async def import_multisig_info(self, *, info: list[str]) -> dict[str, Any]:
        """
        Import multisig info from other participants.

        Parameters
        ----------
        info : list[str]
            Array of multisig info from other participants.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="import_multisig_info", params={"info": info}
        )

    async def finalize_multisig(
        self, *, multisig_info: list[str], password: str
    ) -> dict[str, Any]:
        """
        Finalize a multisig wallet.

        Parameters
        ----------
        multisig_info : list[str]
            Array of multisig info from other participants.
        password : str
            Wallet password.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="finalize_multisig",
            params={"multisig_info": multisig_info, "password": password},
        )

    async def exchange_multisig_keys(
        self, *, multisig_info: list[str], password: str
    ) -> dict[str, Any]:
        """
        Exchange multisig keys with other participants.

        Parameters
        ----------
        multisig_info : list[str]
            Array of multisig info from other participants.
        password : str
            Wallet password.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="exchange_multisig_keys",
            params={"multisig_info": multisig_info, "password": password},
        )

    async def sign_multisig(self, *, tx_data_hex: str) -> dict[str, Any]:
        """
        Sign a multisig transaction.

        Parameters
        ----------
        tx_data_hex : str
            Transaction in hex format.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="sign_multisig", params={"tx_data_hex": tx_data_hex}
        )

    async def submit_multisig(self, *, tx_data_hex: str) -> dict[str, Any]:
        """
        Submit a signed multisig transaction.

        Parameters
        ----------
        tx_data_hex : str
            Transaction in hex format.

        Returns
        -------
        dict[str, Any]
            The submitted transaction.

        """
        return await self._request(
            method="submit_multisig", params={"tx_data_hex": tx_data_hex}
        )

    async def validate_address(
        self,
        *,
        address: str,
        any_net_type: Optional[bool] = False,
        allow_openalias: Optional[bool] = False,
    ) -> dict[str, Any]:
        """
        Validate a public address.

        Parameters
        ----------
        address : str
            Public address.
        any_net_type : bool, optional
            Allow any net type.
        allow_openalias : bool, optional
            Allow OpenAlias addresses.


        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="validate_address",
            params={
                "address": address,
                "any_net_type": any_net_type,
                "allow_openalias": allow_openalias,
            },
        )

    async def set_daemon(
        self,
        *,
        address: str,
        trusted: bool,
        ssl_support: Optional[str] = "autodetect",
        ssl_private_key_path: Optional[str] = None,
        ssl_certificate_path: Optional[str] = None,
        ssl_ca_file: Optional[str] = None,
        ssl_allowed_fingerprints: Optional[list[str]] = None,
        ssl_allow_any_cert: Optional[bool] = False,
    ) -> dict[str, Any]:
        """
        Set the daemon address.

        Parameters
        ----------
        address : str
            Daemon public address.
        trusted : bool
            If true, trust the daemon.
        ssl_support : str, optional
            SSL support (autodetect, enabled, disabled).
        ssl_private_key_path : str, optional
            SSL private key path.
        ssl_certificate_path : str, optional
            SSL certificate path.
        ssl_ca_file : str, optional
            SSL CA file.
        ssl_allowed_fingerprints : list[str], optional
            SSL allowed fingerprints.
        ssl_allow_any_cert : bool, optional
            Allow any certificate.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="set_daemon",
            params={
                "address": address,
                "trusted": trusted,
                "ssl_support": ssl_support,
                "ssl_private_key_path": ssl_private_key_path,
                "ssl_certificate_path": ssl_certificate_path,
                "ssl_ca_file": ssl_ca_file,
                "ssl_allowed_fingerprints": ssl_allowed_fingerprints,
                "ssl_allow_any_cert": ssl_allow_any_cert,
            },
        )

    async def set_log_level(self, *, level: int) -> dict[str, Any]:
        """
        Set the log level.

        Parameters
        ----------
        level : int
            Log level.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="set_log_level", params={"level": level})

    async def set_log_categories(self, *, categories: str) -> dict[str, Any]:
        """
        Set the log categories.

        Parameters
        ----------
        categories : str
            Log categories.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(
            method="set_log_categories", params={"categories": categories}
        )

    async def get_version(self) -> dict[str, Any]:
        """
        Get the wallet version.

        Returns
        -------
        dict[str, Any]
            The response from wallet RPC.

        """
        return await self._request(method="get_version", params={})
