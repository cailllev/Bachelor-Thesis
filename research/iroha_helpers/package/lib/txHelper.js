"use strict";
exports.__esModule = true;
var tslib_1 = require("tslib");
var buffer_1 = require("buffer");
var js_sha3_1 = require("js-sha3");
var lodash_clonedeep_1 = tslib_1.__importDefault(require("lodash.clonedeep"));
var Commands = tslib_1.__importStar(require("./proto/commands_pb"));
var endpoint_pb_1 = require("./proto/endpoint_pb");
var primitive_pb_1 = require("./proto/primitive_pb");
var Transaction = tslib_1.__importStar(require("./proto/transaction_pb"));
var util_js_1 = require("./util.js");
var cryptoHelper_1 = tslib_1.__importDefault(require("./cryptoHelper"));
/**
 * Returns new transactions
 * @returns {Object} transaction
 */
var emptyTransaction = function () { return new Transaction.Transaction(); };
/**
 * Returns payload from the transaction or a new one
 * @param {Object} transaction
 */
var getOrCreatePayload = function (transaction) { return transaction.hasPayload()
    ? lodash_clonedeep_1["default"](transaction.getPayload())
    : new Transaction.Transaction.Payload(); };
/**
 * Returns reducedPayload from the payload or a new one
 * @param {Object} payload
 */
var getOrCreateReducedPayload = function (payload) { return payload.hasReducedPayload()
    ? lodash_clonedeep_1["default"](payload.getReducedPayload())
    : new Transaction.Transaction.Payload.ReducedPayload(); };
// TODO: Create corner cases for AddPeer, setPermission
/**
 * Returns new query with added command.
 * @param {Object} transaction base transaction
 * @param {String} commandName name of a commandName. For reference, visit http://iroha.readthedocs.io/en/latest/develop/api/commands.html
 * @param {Object} params command parameters. For reference, visit http://iroha.readthedocs.io/en/latest/develop/api/commands.html
 * @returns {Object} transaction with commands
 */
var addCommand = function (transaction, commandName, params) {
    var payloadCommand = new Commands[util_js_1.capitalize(commandName)]();
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    for (var _i = 0, _a = Object.entries(params); _i < _a.length; _i++) {
        var _b = _a[_i], key = _b[0], value = _b[1];
        if ('set' + util_js_1.capitalize(key) === 'setPeer') {
            var peer = new primitive_pb_1.Peer();
            peer.setAddress(value.address);
            peer.setPeerKey(value.peerKey);
            payloadCommand['set' + util_js_1.capitalize(key)](peer);
        }
        else {
            payloadCommand['set' + util_js_1.capitalize(key)](value);
        }
    }
    var command = new Commands.Command();
    var commandNameSetter = 'set' + util_js_1.capitalize(commandName);
    command[commandNameSetter](payloadCommand);
    var payload = getOrCreatePayload(transaction);
    var reducedPayload = getOrCreateReducedPayload(payload);
    reducedPayload.addCommands(command, reducedPayload.getCommandsList.length);
    payload.setReducedPayload(reducedPayload);
    var txWithCommand = lodash_clonedeep_1["default"](transaction);
    txWithCommand.setPayload(payload);
    return txWithCommand;
};
/**
 * Returns new transaction with meta information
 * @param {Object} transaction base transaction
 * @param {Object} meta - meta info
 * @param {String} meta.creatorAccountId accountID of transaction's creator
 * @param {Number} meta.createdTime time of transaction creation
 * @param {Number} meta.quorum minimum amount of signatures needed to sign a transaction
 */
var addMeta = function (transaction, _a) {
    var creatorAccountId = _a.creatorAccountId, _b = _a.createdTime, createdTime = _b === void 0 ? Date.now() : _b, _c = _a.quorum, quorum = _c === void 0 ? 1 : _c;
    var payload = getOrCreatePayload(transaction);
    var reducedPayload = getOrCreateReducedPayload(payload);
    reducedPayload.setCreatorAccountId(creatorAccountId);
    reducedPayload.setCreatedTime(createdTime);
    reducedPayload.setQuorum(quorum);
    payload.setReducedPayload(reducedPayload);
    var transactionWithMeta = lodash_clonedeep_1["default"](transaction);
    transactionWithMeta.setPayload(payload);
    return transactionWithMeta;
};
/**
 * Returns buffer hash of a transaction
 * @param {Object} transaction base transaction
 * @returns {Buffer} transaction hash
 */
var hash = function (transaction) {
    return buffer_1.Buffer.from(js_sha3_1.sha3_256.array(transaction.getPayload().serializeBinary()));
};
/**
 * Returns new transaction with one more signature
 * @param {Object} transaction base transaction
 * @param {String} privateKeyHex - private key of query's creator in hex.
 */
var sign = function (transaction, privateKeyHex) {
    var privateKey = buffer_1.Buffer.from(privateKeyHex, 'hex');
    var publicKey = cryptoHelper_1["default"].derivePublicKey(privateKeyHex);
    var payloadHash = hash(transaction);
    var signatory = cryptoHelper_1["default"].sign(payloadHash, publicKey, privateKey);
    var s = new primitive_pb_1.Signature();
    s.setPublicKey(publicKey.toString('hex'));
    s.setSignature(signatory.toString('hex'));
    var signedTransactionWithSignature = lodash_clonedeep_1["default"](transaction);
    signedTransactionWithSignature.addSignatures(s, signedTransactionWithSignature.getSignaturesList.length);
    return signedTransactionWithSignature;
};
/**
 * Returns array of transactions with Batch Meta in them
 * @param {Array} transactions transactions to be included in batch
 * @param {Number} type type of batch transaction, 0 for ATOMIC, 1 for ORDERED
 * @returns {Array} Transactions with all necessary fields
 */
var addBatchMeta = function (transactions, type) {
    var reducedHashes = transactions.map(function (tx) { return js_sha3_1.sha3_256(tx.getPayload().getReducedPayload().serializeBinary()); });
    var batchMeta = new Transaction.Transaction.Payload.BatchMeta();
    batchMeta.setReducedHashesList(reducedHashes);
    batchMeta.setType(type);
    var transactionsWithBatchMeta = transactions.map(function (tx) {
        var transaction = lodash_clonedeep_1["default"](tx);
        var payload = getOrCreatePayload(transaction);
        payload.setBatch(batchMeta);
        transaction.setPayload(payload);
        return transaction;
    });
    return transactionsWithBatchMeta;
};
/**
 * Returns a TransactionList with transactions from array
 * @param {Array} transactions transactions to be included in batch
 * @returns {Object} TxList with all transactions
 */
var createTxListFromArray = function (transactions) {
    var txList = new endpoint_pb_1.TxList();
    txList.setTransactionsList(transactions);
    return txList;
};
// TODO: Add types for commands
exports["default"] = {
    addCommand: addCommand,
    addMeta: addMeta,
    sign: sign,
    emptyTransaction: emptyTransaction,
    hash: hash,
    addBatchMeta: addBatchMeta,
    createTxListFromArray: createTxListFromArray
};
//# sourceMappingURL=txHelper.js.map