"use strict";
exports.__esModule = true;
exports.BatchBuilder = exports.TxBuilder = void 0;
var tslib_1 = require("tslib");
var txHelper_1 = tslib_1.__importDefault(require("./txHelper"));
var validation_1 = tslib_1.__importDefault(require("./validation"));
var util_1 = require("./util");
var Transaction = tslib_1.__importStar(require("./proto/transaction_pb"));
var Chain = /** @class */ (function () {
    function Chain(txs) {
        this.txs = txs;
    }
    Chain.prototype.sign = function (privateKeys, transactionId) {
        var signed = privateKeys.reduce(function (tx, key) { return txHelper_1["default"].sign(tx, key); }, this.txs[transactionId]);
        var newTxs = this.txs.slice();
        newTxs.splice(transactionId, 1, signed);
        return new Chain(newTxs);
    };
    Chain.prototype.send = function (commandService, timeoutLimit, statusesList) {
        if (timeoutLimit === void 0) { timeoutLimit = 5000; }
        if (statusesList === void 0) { statusesList = []; }
        return util_1.sendTransactions(this.txs, commandService, timeoutLimit, statusesList);
    };
    return Chain;
}());
var TxBuilder = /** @class */ (function () {
    function TxBuilder(tx) {
        if (tx === void 0) { tx = new Transaction.Transaction(); }
        this.tx = tx;
    }
    TxBuilder.prototype.addAssetQuantity = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'addAssetQuantity', validation_1["default"](params, ['assetId', 'amount'])));
    };
    TxBuilder.prototype.addPeer = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'addPeer', validation_1["default"](params, ['address', 'peerKey'])));
    };
    TxBuilder.prototype.addSignatory = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'addSignatory', validation_1["default"](params, ['accountId', 'publicKey'])));
    };
    TxBuilder.prototype.callEngine = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'callEngine', validation_1["default"](params, ['type', 'caller', 'callee', 'input'])));
    };
    TxBuilder.prototype.createAsset = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'createAsset', validation_1["default"](params, ['assetName', 'domainId', 'precision'])));
    };
    TxBuilder.prototype.createAccount = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'createAccount', validation_1["default"](params, ['accountName', 'domainId', 'publicKey'])));
    };
    TxBuilder.prototype.setAccountDetail = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'setAccountDetail', validation_1["default"](params, ['accountId', 'key', 'value'])));
    };
    TxBuilder.prototype.createDomain = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'createDomain', validation_1["default"](params, ['domainId', 'defaultRole'])));
    };
    TxBuilder.prototype.removeSignatory = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'removeSignatory', validation_1["default"](params, ['accountId', 'publicKey'])));
    };
    TxBuilder.prototype.setAccountQuorum = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'setAccountQuorum', validation_1["default"](params, ['accountId', 'quorum'])));
    };
    TxBuilder.prototype.transferAsset = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'transferAsset', validation_1["default"](params, ['amount', 'assetId', 'description', 'destAccountId', 'srcAccountId'])));
    };
    TxBuilder.prototype.appendRole = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'appendRole', validation_1["default"](params, ['accountId', 'roleName'])));
    };
    TxBuilder.prototype.detachRole = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'detachRole', validation_1["default"](params, ['accountId', 'roleName'])));
    };
    TxBuilder.prototype.createRole = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'createRole', validation_1["default"](params, ['roleName', 'permissionsList'])));
    };
    TxBuilder.prototype.grantPermission = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'grantPermission', validation_1["default"](params, ['accountId', 'permission'])));
    };
    TxBuilder.prototype.revokePermission = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'revokePermission', validation_1["default"](params, ['accountId', 'permission'])));
    };
    TxBuilder.prototype.subtractAssetQuantity = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'subtractAssetQuantity', validation_1["default"](params, ['assetId', 'amount'])));
    };
    TxBuilder.prototype.compareAndSetAccountDetail = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'compareAndSetAccountDetail', validation_1["default"](params, ['accountId', 'key', 'value', 'oldValue'])));
    };
    TxBuilder.prototype.setSettingValue = function () {
        throw new Error('Command not allowed to use');
    };
    TxBuilder.prototype.removePeer = function (params) {
        return new TxBuilder(txHelper_1["default"].addCommand(this.tx, 'removePeer', validation_1["default"](params, ['publicKey'])));
    };
    TxBuilder.prototype.addMeta = function (creatorAccountId, quorum) {
        return new TxBuilder(txHelper_1["default"].addMeta(this.tx, { creatorAccountId: creatorAccountId, quorum: quorum }));
    };
    TxBuilder.prototype.sign = function (privateKeys) {
        return new TxBuilder(privateKeys.reduce(function (tx, key) { return txHelper_1["default"].sign(tx, key); }, this.tx));
    };
    TxBuilder.prototype.send = function (commandService, timeoutLimit, statusesList) {
        if (timeoutLimit === void 0) { timeoutLimit = 5000; }
        if (statusesList === void 0) { statusesList = []; }
        return util_1.sendTransactions([this.tx], commandService, timeoutLimit, statusesList);
    };
    return TxBuilder;
}());
exports.TxBuilder = TxBuilder;
var BatchBuilder = /** @class */ (function () {
    function BatchBuilder(txs) {
        this.txs = txs;
    }
    BatchBuilder.prototype.addTransaction = function (tx) {
        return new BatchBuilder(tslib_1.__spreadArrays(this.txs, [tx]));
    };
    /**
     * 0 - ATOMIC
     * 1 - ORDERED
     */
    BatchBuilder.prototype.setBatchMeta = function (type) {
        return new Chain(txHelper_1["default"].addBatchMeta(this.txs, type));
    };
    return BatchBuilder;
}());
exports.BatchBuilder = BatchBuilder;
//# sourceMappingURL=chain.js.map