"use strict";
exports.__esModule = true;
exports.signWithArrayOfKeys = exports.sendTransactions = exports.reverseEnum = exports.capitalize = void 0;
var tslib_1 = require("tslib");
var txHelper_1 = tslib_1.__importDefault(require("./txHelper"));
var endpoint_pb_1 = require("./proto/endpoint_pb");
function _listToTorii(txs, txClient, timeoutLimit) {
    var txList = txHelper_1["default"].createTxListFromArray(txs);
    return new Promise(function (resolve, reject) {
        /**
         * grpc-node hangs against unresponsive server, which possibly occur when
         * invalid node IP is set. To avoid this problem, we use timeout timer.
         * c.f. {@link https://github.com/grpc/grpc/issues/13163 Grpc issue 13163}
         */
        var timer = setTimeout(function () {
            txClient.$channel.close();
            reject(new Error('Please check IP address OR your internet connection'));
        }, timeoutLimit);
        // Sending even 1 transaction to listTorii is absolutely ok and valid.
        txClient.listTorii(txList, function (err) {
            clearTimeout(timer);
            if (err) {
                return reject(err);
            }
            var hashes = txs.map(function (x) { return txHelper_1["default"].hash(x); });
            resolve(hashes);
        });
    });
}
function _handleStream(hash, txClient) {
    var request = new endpoint_pb_1.TxStatusRequest();
    request.setTxHash(hash.toString('hex'));
    return txClient.statusStream(request);
}
function _fromStream(_a, requiredStatusesStr) {
    var hash = _a.hash, txClient = _a.txClient;
    var terminalStatuses = [
        endpoint_pb_1.TxStatus.STATELESS_VALIDATION_FAILED,
        endpoint_pb_1.TxStatus.STATEFUL_VALIDATION_FAILED,
        endpoint_pb_1.TxStatus.COMMITTED,
        endpoint_pb_1.TxStatus.NOT_RECEIVED,
        endpoint_pb_1.TxStatus.REJECTED
    ];
    var requiredStatuses = requiredStatusesStr.map(function (s) { return endpoint_pb_1.TxStatus[s]; });
    var successStatuses = tslib_1.__spreadArrays([
        endpoint_pb_1.TxStatus.COMMITTED
    ], requiredStatuses);
    var isTerminal = function (status) { return terminalStatuses.includes(status); };
    var isRequired = function (status) { return requiredStatuses.includes(status); };
    var isError = function (status) { return !successStatuses.includes(status); };
    return new Promise(function (resolve) {
        var timer;
        var connect = function () {
            var stream = _handleStream(hash, txClient);
            stream.on('data', dataHandler);
        };
        var resetTimer = function () {
            clearTimeout(timer);
            timer = setTimeout(connect, 5000);
        };
        var dataHandler = function (tx) {
            resetTimer();
            var status = tx.getTxStatus();
            if (isTerminal(status) || isRequired(status)) {
                clearTimeout(timer);
                resolve({
                    tx: tx,
                    error: isError(status)
                });
            }
        };
        connect();
    });
}
function _streamVerifier(hash, txClient, requiredStatusesStr) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var result;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, _fromStream({ hash: hash, txClient: txClient }, requiredStatusesStr)];
                case 1:
                    result = _a.sent();
                    return [2 /*return*/, result];
            }
        });
    });
}
/**
 * Capitalizes string
 * @param {String} string
 * @returns {String} capitalized string
 */
var capitalize = function (string) { return string.charAt(0).toUpperCase() + string.slice(1); };
exports.capitalize = capitalize;
function reverseEnum(e) {
    var rmap = {};
    for (var _i = 0, _a = Object.entries(e); _i < _a.length; _i++) {
        var _b = _a[_i], key = _b[0], value = _b[1];
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        rmap[value] = key;
    }
    return rmap;
}
exports.reverseEnum = reverseEnum;
function sendTransactions(txs, txClient, timeoutLimit, requiredStatusesStr) {
    if (requiredStatusesStr === void 0) { requiredStatusesStr = [
        'COMMITTED'
    ]; }
    return _listToTorii(txs, txClient, timeoutLimit)
        .then(function (hashes) {
        return new Promise(function (resolve, reject) {
            var requests = hashes
                .map(function (h) { return _streamVerifier(h, txClient, requiredStatusesStr); });
            Promise.all(requests)
                .then(function (res) {
                var status = res
                    .map(function (r) { return reverseEnum(endpoint_pb_1.TxStatus)[r.tx.getTxStatus()]; });
                return res.some(function (r) { return r.error; })
                    ? reject(new Error("Command response error: expected=" + requiredStatusesStr + ", actual=" + status))
                    : resolve();
            });
        });
    });
}
exports.sendTransactions = sendTransactions;
function signWithArrayOfKeys(tx, privateKeys) {
    privateKeys.forEach(function (key) {
        tx = txHelper_1["default"].sign(tx, key);
    });
    return tx;
}
exports.signWithArrayOfKeys = signWithArrayOfKeys;
//# sourceMappingURL=util.js.map