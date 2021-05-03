"use strict";
exports.__esModule = true;
var tslib_1 = require("tslib");
var lodash_flow_1 = tslib_1.__importDefault(require("lodash.flow"));
var queryHelper_1 = tslib_1.__importDefault(require("../queryHelper"));
var pbResponse = tslib_1.__importStar(require("../proto/qry_responses_pb"));
var util_1 = require("../util");
var validation_1 = tslib_1.__importDefault(require("../validation"));
var DEFAULT_OPTIONS = {
    privateKey: '',
    creatorAccountId: '',
    queryService: null,
    timeoutLimit: 5000
};
/**
 * wrapper function of queries
 * @param {Object} queryOptions
 * @param {Object} query
 * @param {Function} onResponse
 */
function sendQuery(_a, query, 
// eslint-disable-next-line
onResponse) {
    var _b = _a === void 0 ? DEFAULT_OPTIONS : _a, privateKey = _b.privateKey, creatorAccountId = _b.creatorAccountId, queryService = _b.queryService, timeoutLimit = _b.timeoutLimit;
    if (onResponse === void 0) { onResponse = function (resolve, reject, responseName, response) { }; }
    return new Promise(function (resolve, reject) {
        var queryClient = queryService;
        var queryToSend = lodash_flow_1["default"](function (q) { return queryHelper_1["default"].addMeta(q, { creatorAccountId: creatorAccountId }); }, function (q) { return queryHelper_1["default"].sign(q, privateKey); })(query);
        /**
         * grpc-node hangs against unresponsive server, which possibly occur when
         * invalid node IP is set. To avoid this problem, we use timeout timer.
         * c.f. {@link https://github.com/grpc/grpc/issues/13163 Grpc issue 13163}
         */
        var timer = setTimeout(function () {
            queryClient.$channel.close();
            reject(new Error('please check IP address OR your internet connection'));
        }, timeoutLimit);
        queryClient.find(queryToSend, function (err, response) {
            clearTimeout(timer);
            if (err) {
                return reject(err);
            }
            var type = response.getResponseCase();
            var responseName = util_1.reverseEnum(pbResponse.QueryResponse.ResponseCase)[type];
            onResponse(resolve, reject, responseName, response);
        });
    });
}
/**
 * getAccount
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-account
 */
function getAccount(queryOptions, params) {
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getAccount', validation_1["default"](params, ['accountId'])), function (resolve, reject, responseName, response) {
        if (responseName !== 'ACCOUNT_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=ACCOUNT_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var account = response.getAccountResponse().getAccount().toObject();
        resolve(account);
    });
}
/**
 * getRawAccount
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-account
 */
function getRawAccount(queryOptions, params) {
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getAccount', validation_1["default"](params, ['accountId'])), function (resolve, reject, responseName, response) {
        if (responseName !== 'ACCOUNT_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=ACCOUNT_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var account = response.getAccountResponse();
        resolve(account);
    });
}
/**
 * getSignatories
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-signatories
 */
function getSignatories(queryOptions, params) {
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getSignatories', validation_1["default"](params, ['accountId'])), function (resolve, reject, responseName, response) {
        if (responseName !== 'SIGNATORIES_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=SIGNATORIES_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var account = response.getSignatoriesResponse().toObject().keysList;
        resolve(account);
    });
}
/**
 * getTransactions
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String[]} params.txHashesList
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-transactions
 */
function getTransactions(queryOptions, params) {
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getTransactions', validation_1["default"](params, ['txHashesList'])), function (resolve, reject, responseName, response) {
        if (responseName !== 'TRANSACTIONS_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=TRANSACTIONS_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var transactions = response.getTransactionsResponse();
        resolve(transactions);
    });
}
/**
 * getPendingTransactions
 * @param {Object} queryOptions
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-pending-transactions
 */
function getPendingTransactions(queryOptions, _a) {
    var pageSize = _a.pageSize, firstTxHash = _a.firstTxHash, _b = _a.ordering, field = _b.field, direction = _b.direction;
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getPendingTransactions', {
        paginationMeta: {
            pageSize: pageSize,
            firstTxHash: firstTxHash,
            ordering: {
                field: field,
                direction: direction
            }
        }
    }), function (resolve, reject, responseName, response) {
        if (responseName !== 'PENDING_TRANSACTIONS_PAGE_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=PENDING_TRANSACTIONS_PAGE_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var transactions = response.getPendingTransactionsPageResponse().toObject().transactionsList;
        resolve(transactions);
    });
}
/**
 * getRawPendingTransactions
 * @param {Object} queryOptions
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-pending-transactions
 */
function getRawPendingTransactions(queryOptions) {
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getPendingTransactions'), function (resolve, reject, responseName, response) {
        if (responseName !== 'PENDING_TRANSACTIONS_PAGE_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=PENDING_TRANSACTIONS_PAGE_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var transactions = response.getPendingTransactionsPageResponse();
        resolve(transactions);
    });
}
/**
 * getAccountTransactions
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {Number} params.pageSize
 * @property {String | undefined} params.firstTxHash
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-account-transactions
 */
function getAccountTransactions(queryOptions, _a) {
    var accountId = _a.accountId, pageSize = _a.pageSize, firstTxHash = _a.firstTxHash, _b = _a.ordering, field = _b.field, direction = _b.direction;
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getAccountTransactions', {
        accountId: accountId,
        paginationMeta: {
            pageSize: pageSize,
            firstTxHash: firstTxHash,
            ordering: {
                field: field,
                direction: direction
            }
        }
    }), function (resolve, reject, responseName, response) {
        if (responseName !== 'TRANSACTIONS_PAGE_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=TRANSACTIONS_PAGE_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var transactions = response.getTransactionsPageResponse().toObject();
        resolve(transactions);
    });
}
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
function getAccountAssetTransactions(queryOptions, _a) {
    var accountId = _a.accountId, assetId = _a.assetId, pageSize = _a.pageSize, firstTxHash = _a.firstTxHash, _b = _a.ordering, field = _b.field, direction = _b.direction;
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getAccountAssetTransactions', {
        accountId: accountId,
        assetId: assetId,
        paginationMeta: {
            pageSize: pageSize,
            firstTxHash: firstTxHash,
            ordering: {
                field: field,
                direction: direction
            }
        }
    }), function (resolve, reject, responseName, response) {
        if (responseName !== 'TRANSACTIONS_PAGE_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=TRANSACTIONS_PAGE_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var transactions = response.getTransactionsPageResponse().toObject();
        resolve(transactions);
    });
}
/**
 * getAccountAssets
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-account-assets
 */
function getAccountAssets(queryOptions, _a) {
    var accountId = _a.accountId, pageSize = _a.pageSize, firstAssetId = _a.firstAssetId;
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getAccountAssets', {
        accountId: accountId,
        paginationMeta: {
            pageSize: pageSize,
            firstAssetId: firstAssetId
        }
    }), function (resolve, reject, responseName, response) {
        if (responseName !== 'ACCOUNT_ASSETS_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=ACCOUNT_ASSETS_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var assets = response.getAccountAssetsResponse().toObject().accountAssetsList;
        resolve(assets);
    });
}
/**
 * getAccountDetail
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.key
 * @property {String} params.writer
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-account-detail
 */
function getAccountDetail(queryOptions, _a) {
    var accountId = _a.accountId, key = _a.key, writer = _a.writer, pageSize = _a.pageSize, paginationWriter = _a.paginationWriter, paginationKey = _a.paginationKey;
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getAccountDetail', {
        accountId: accountId,
        key: key,
        writer: writer,
        paginationMeta: {
            pageSize: pageSize,
            firstRecordId: {
                writer: paginationWriter,
                key: paginationKey
            }
        }
    }), function (resolve, reject, responseName, response) {
        if (responseName !== 'ACCOUNT_DETAIL_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=ACCOUNT_DETAIL_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var transactions = JSON.parse(response.getAccountDetailResponse().toObject().detail);
        resolve(transactions);
    });
}
/**
 * getAssetInfo
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {String} params.assetId
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-asset-info
 */
function getAssetInfo(queryOptions, params) {
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getAssetInfo', validation_1["default"](params, ['assetId'])), function (resolve, reject, responseName, response) {
        if (responseName !== 'ASSET_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=ASSET_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var info = response.getAssetResponse().toObject().asset;
        resolve(info);
    });
}
/**
 * getPeers
 * @param {Object} queryOptions
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-peers
 */
function getPeers(queryOptions) {
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getPeers'), function (resolve, reject, responseName, response) {
        if (responseName !== 'PEERS_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=PEERS_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var peers = response.getPeersResponse().toObject().peersList;
        resolve(peers);
    });
}
/**
 * getRoles
 * @param {Object} queryOptions
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-roles
 */
function getRoles(queryOptions) {
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getRoles'), function (resolve, reject, responseName, response) {
        if (responseName !== 'ROLES_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=ROLES_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var roles = response.getRolesResponse().toObject().rolesList;
        resolve(roles);
    });
}
/**
 * getRolePermissions
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {Number} params.roleId
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-role-permissions
 */
function getRolePermissions(queryOptions, params) {
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getRolePermissions', validation_1["default"](params, ['roleId'])), function (resolve, reject, responseName, response) {
        if (responseName !== 'ROLE_PERMISSIONS_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=ROLE_PERMISSIONS_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var permissions = response.getRolePermissionsResponse().toObject().permissionsList;
        resolve(permissions);
    });
}
/**
 * getBlock
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {Number} params.height
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-block
 */
function getBlock(queryOptions, params) {
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getBlock', validation_1["default"](params, ['height'])), function (resolve, reject, responseName, response) {
        if (responseName !== 'BLOCK_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=BLOCK_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var block = response.getBlockResponse().toObject().block.blockV1;
        resolve(block);
    });
}
/**
 * getEngineReceipts
 * @param {Object} queryOptions
 * @param {Object} params
 * @property {Number} params.txHash
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#get-block
 */
function getEngineReceipts(queryOptions, params) {
    return sendQuery(queryOptions, queryHelper_1["default"].addQuery(queryHelper_1["default"].emptyQuery(), 'getEngineReceipts', validation_1["default"](params, ['txHash'])), function (resolve, reject, responseName, response) {
        if (responseName !== 'ENGINE_RECEIPTS_RESPONSE') {
            var error = JSON.stringify(response.toObject().errorResponse);
            return reject(new Error("Query response error: expected=ENGINE_RECEIPTS_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        var block = response.getEngineReceiptsResponse();
        resolve(block);
    });
}
/**
 * fetchCommits
 * @param {Object} queryOptions
 * @param {Function} onBlock
 * @param {Function} onError
 * @link https://iroha.readthedocs.io/en/master/develop/api/queries.html#fetchcommits
 */
function fetchCommits(_a, 
// eslint-disable-next-line
onBlock, 
// eslint-disable-next-line
onError) {
    var _b = _a === void 0 ? DEFAULT_OPTIONS : _a, privateKey = _b.privateKey, creatorAccountId = _b.creatorAccountId, queryService = _b.queryService;
    if (onBlock === void 0) { onBlock = function (block) { }; }
    if (onError === void 0) { onError = function (error) { }; }
    var query = queryHelper_1["default"].emptyBlocksQuery();
    var queryToSend = lodash_flow_1["default"](function (q) { return queryHelper_1["default"].addMeta(q, { creatorAccountId: creatorAccountId }); }, function (q) { return queryHelper_1["default"].sign(q, privateKey); })(query);
    var stream = queryService.fetchCommits(queryToSend);
    stream.on('data', function (response) {
        var type = response.getResponseCase();
        var responseName = util_1.reverseEnum(pbResponse.BlockQueryResponse.ResponseCase)[type];
        if (responseName !== 'BLOCK_RESPONSE') {
            var error = JSON.stringify(response.toObject().blockErrorResponse);
            onError(new Error("Query response error: expected=BLOCK_RESPONSE, actual=" + responseName + "\nReason: " + error));
        }
        else {
            var block = response.toObject().blockResponse.block;
            onBlock(block);
        }
    });
}
exports["default"] = {
    getAccount: getAccount,
    getRawAccount: getRawAccount,
    getSignatories: getSignatories,
    getTransactions: getTransactions,
    getPendingTransactions: getPendingTransactions,
    getRawPendingTransactions: getRawPendingTransactions,
    getAccountTransactions: getAccountTransactions,
    getAccountAssetTransactions: getAccountAssetTransactions,
    getAccountAssets: getAccountAssets,
    getAccountDetail: getAccountDetail,
    getAssetInfo: getAssetInfo,
    getPeers: getPeers,
    getRoles: getRoles,
    getRolePermissions: getRolePermissions,
    getBlock: getBlock,
    getEngineReceipts: getEngineReceipts,
    fetchCommits: fetchCommits
};
//# sourceMappingURL=index.js.map