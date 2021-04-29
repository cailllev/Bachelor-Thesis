/**
 * getAccount
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-account
 */
declare function getAccount(queryOptions: any, params: any): Promise<unknown>;
/**
 * getRawAccount
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-account
 */
declare function getRawAccount(queryOptions: any, params: any): Promise<unknown>;
/**
 * getSignatories
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-signatories
 */
declare function getSignatories(queryOptions: any, params: any): Promise<unknown>;
/**
 * getTransactions
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String[]} params.txHashesList
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-transactions
 */
declare function getTransactions(queryOptions: any, params: any): Promise<unknown>;
/**
 * getPendingTransactions
 * @param {Object} queryOptions
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-pending-transactions
 */
declare function getPendingTransactions(queryOptions: any, { pageSize, firstTxHash, ordering: { field, direction } }: {
    pageSize: any;
    firstTxHash: any;
    ordering: {
        field: any;
        direction: any;
    };
}): Promise<unknown>;
/**
 * getRawPendingTransactions
 * @param {Object} queryOptions
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-pending-transactions
 */
declare function getRawPendingTransactions(queryOptions: any): Promise<unknown>;
/**
 * getAccountTransactions
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {Number} params.pageSize
 * @property {String | undefined} params.firstTxHash
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-account-transactions
 */
declare function getAccountTransactions(queryOptions: any, { accountId, pageSize, firstTxHash, ordering: { field, direction } }: {
    accountId: any;
    pageSize: any;
    firstTxHash: any;
    ordering: {
        field: any;
        direction: any;
    };
}): Promise<unknown>;
/**
 * getAccountAssetTransactions
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.assetId
 * @property {Number} params.pageSize
 * @property {String | undefined} params.firstTxHash
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-account-asset-transactions
 */
declare function getAccountAssetTransactions(queryOptions: any, { accountId, assetId, pageSize, firstTxHash, ordering: { field, direction } }: {
    accountId: any;
    assetId: any;
    pageSize: any;
    firstTxHash: any;
    ordering: {
        field: any;
        direction: any;
    };
}): Promise<unknown>;
/**
 * getAccountAssets
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-account-assets
 */
declare function getAccountAssets(queryOptions: any, { accountId, pageSize, firstAssetId }: {
    accountId: any;
    pageSize: any;
    firstAssetId: any;
}): Promise<unknown>;
/**
 * getAccountDetail
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.key
 * @property {String} params.writer
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-account-detail
 */
declare function getAccountDetail(queryOptions: any, { accountId, key, writer, pageSize, paginationWriter, paginationKey }: {
    accountId: any;
    key: any;
    writer: any;
    pageSize: any;
    paginationWriter: any;
    paginationKey: any;
}): Promise<unknown>;
/**
 * getAssetInfo
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.assetId
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-asset-info
 */
declare function getAssetInfo(queryOptions: any, params: any): Promise<unknown>;
/**
 * getPeers
 * @param {Object} queryOptions
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-peers
 */
declare function getPeers(queryOptions: any): Promise<unknown>;
/**
 * getRoles
 * @param {Object} queryOptions
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-roles
 */
declare function getRoles(queryOptions: any): Promise<unknown>;
/**
 * getRolePermissions
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {Number} params.roleId
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-role-permissions
 */
declare function getRolePermissions(queryOptions: any, params: any): Promise<unknown>;
/**
 * getBlock
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {Number} params.height
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-block
 */
declare function getBlock(queryOptions: any, params: any): Promise<unknown>;
/**
 * getEngineReceipts
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {Number} params.txHash
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-block
 */
declare function getEngineReceipts(queryOptions: any, params: any): Promise<unknown>;
/**
 * fetchCommits
 * @param {Object} queryOptions
 * @param {Function} onBlock
 * @param {Function} onError
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#fetchcommits
 */
declare function fetchCommits({ privateKey, creatorAccountId, queryService }?: {
    privateKey: string;
    creatorAccountId: string;
    queryService: any;
    timeoutLimit: number;
}, onBlock?: (block: any) => void, onError?: (error: any) => void): void;
declare const _default: {
    getAccount: typeof getAccount;
    getRawAccount: typeof getRawAccount;
    getSignatories: typeof getSignatories;
    getTransactions: typeof getTransactions;
    getPendingTransactions: typeof getPendingTransactions;
    getRawPendingTransactions: typeof getRawPendingTransactions;
    getAccountTransactions: typeof getAccountTransactions;
    getAccountAssetTransactions: typeof getAccountAssetTransactions;
    getAccountAssets: typeof getAccountAssets;
    getAccountDetail: typeof getAccountDetail;
    getAssetInfo: typeof getAssetInfo;
    getPeers: typeof getPeers;
    getRoles: typeof getRoles;
    getRolePermissions: typeof getRolePermissions;
    getBlock: typeof getBlock;
    getEngineReceipts: typeof getEngineReceipts;
    fetchCommits: typeof fetchCommits;
};
export default _default;
