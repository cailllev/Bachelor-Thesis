"use strict";
exports.__esModule = true;
var tslib_1 = require("tslib");
var buffer_1 = require("buffer");
var js_sha3_1 = require("js-sha3");
var lodash_clonedeep_1 = tslib_1.__importDefault(require("lodash.clonedeep"));
var primitive_pb_1 = require("./proto/primitive_pb");
var Queries = tslib_1.__importStar(require("./proto/queries_pb"));
var util_js_1 = require("./util.js");
var cryptoHelper_1 = tslib_1.__importDefault(require("./cryptoHelper"));
var emptyQuery = function () { return new Queries.Query(); };
var emptyBlocksQuery = function () { return new Queries.BlocksQuery(); };
/**
 * Returns payload from the query or a new one
 * @param {Object} query
 */
var getOrCreatePayload = function (query) { return query.hasPayload()
    ? lodash_clonedeep_1["default"](query.getPayload())
    : new Queries.Query.Payload(); };
/**
 * Returns new query with added command.
 * @param {Object} query base query
 * @param {stringing} queryName name of a query. For reference, visit http://iroha.readthedocs.io/en/latest/develop/api/queries.html
 * @param {Object} params query parameters. For reference, visit http://iroha.readthedocs.io/en/latest/develop/api/queries.html
 */
var addQuery = function (query, queryName, params) {
    if (params === void 0) { params = {}; }
    var payloadQuery = new Queries[util_js_1.capitalize(queryName)]();
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    for (var _i = 0, _a = Object.entries(params); _i < _a.length; _i++) {
        var _b = _a[_i], key = _b[0], value = _b[1];
        var capitalizedKeyName = "set" + util_js_1.capitalize(key);
        if (capitalizedKeyName === 'setPaginationMeta') {
            var paginationMeta = null;
            if (queryName === 'getAccountDetail') {
                var firstRecordId = new primitive_pb_1.AccountDetailRecordId();
                firstRecordId.setKey(value.firstRecordId.key);
                firstRecordId.setWriter(value.firstRecordId.writer);
                paginationMeta = new Queries.AccountDetailPaginationMeta();
                paginationMeta.setPageSize(value.pageSize);
                paginationMeta.setFirstRecordId(firstRecordId);
            }
            else if (queryName === 'getAccountAssets') {
                paginationMeta = new Queries.AssetPaginationMeta();
                paginationMeta.setPageSize(value.pageSize);
                paginationMeta.setFirstAssetId(value.firstAssetId);
            }
            else {
                var queryOrder = new Queries.Ordering();
                var fieldOrder = new Queries.Ordering.FieldOrdering();
                fieldOrder.setField(value.ordering.field);
                fieldOrder.setDirection(value.ordering.direction);
                queryOrder.addSequence(fieldOrder);
                paginationMeta = new Queries.TxPaginationMeta();
                paginationMeta.setPageSize(value.pageSize);
                paginationMeta.setFirstTxHash(value.firstTxHash);
                paginationMeta.setOrdering(queryOrder);
            }
            payloadQuery[capitalizedKeyName](paginationMeta);
        }
        else {
            payloadQuery[capitalizedKeyName](value);
        }
    }
    var payload = getOrCreatePayload(query);
    payload['set' + util_js_1.capitalize(queryName)](payloadQuery);
    var queryWithQuery = lodash_clonedeep_1["default"](query);
    queryWithQuery.setPayload(payload);
    return queryWithQuery;
};
/**
 * Returns new query with meta information
 * @param {Object} query base query
 * @param {Object} meta - meta info
 * @param {stringing} meta.creatorAccountId accountID of query's creator
 * @param {Number} meta.createdTime time of query creation
 * @param {Number} meta.queryCounter query counter (will be removed soon)
 */
var addMeta = function (query, _a) {
    var creatorAccountId = _a.creatorAccountId, _b = _a.createdTime, createdTime = _b === void 0 ? Date.now() : _b, _c = _a.queryCounter, queryCounter = _c === void 0 ? 1 : _c;
    var meta = new Queries.QueryPayloadMeta();
    meta.setCreatorAccountId(creatorAccountId);
    meta.setCreatedTime(createdTime);
    meta.setQueryCounter(queryCounter);
    var queryWithMeta = lodash_clonedeep_1["default"](query);
    if (query instanceof Queries.Query) {
        var payload = getOrCreatePayload(query);
        payload.setMeta(meta);
        queryWithMeta.setPayload(payload);
    }
    else if (query instanceof Queries.BlocksQuery) {
        queryWithMeta.setMeta(meta);
    }
    else {
        throw new Error('Unknown query type');
    }
    return queryWithMeta;
};
/**
 * Returns new signed query
 * @param {Object} query base query
 * @param {stringing} privateKeyHex - private key of query's creator in hex.
 */
var sign = function (query, privateKeyHex) {
    var privateKey = buffer_1.Buffer.from(privateKeyHex, 'hex');
    var publicKey = cryptoHelper_1["default"].derivePublicKey(privateKeyHex);
    var payload = null;
    if (query instanceof Queries.Query) {
        payload = query.getPayload();
    }
    else if (query instanceof Queries.BlocksQuery) {
        payload = query.getMeta();
    }
    else {
        throw new Error('Unknown query type');
    }
    var payloadHash = buffer_1.Buffer.from(js_sha3_1.sha3_256.array(payload.serializeBinary()));
    var signatory = cryptoHelper_1["default"].sign(payloadHash, publicKey, privateKey);
    var s = new primitive_pb_1.Signature();
    s.setPublicKey(publicKey.toString('hex'));
    s.setSignature(signatory.toString('hex'));
    var signedQueryWithSignature = lodash_clonedeep_1["default"](query);
    signedQueryWithSignature.setSignature(s);
    return signedQueryWithSignature;
};
exports["default"] = {
    sign: sign,
    addMeta: addMeta,
    addQuery: addQuery,
    emptyQuery: emptyQuery,
    emptyBlocksQuery: emptyBlocksQuery
};
//# sourceMappingURL=queryHelper.js.map