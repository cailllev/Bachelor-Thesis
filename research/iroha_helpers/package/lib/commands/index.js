"use strict";
exports.__esModule = true;
var tslib_1 = require("tslib");
var txHelper_1 = tslib_1.__importDefault(require("../txHelper"));
var util_1 = require("../util");
var validation_1 = tslib_1.__importDefault(require("../validation"));
var commands_pb_1 = require("../proto/commands_pb");
var DEFAULT_OPTIONS = {
    privateKeys: [''],
    creatorAccountId: '',
    quorum: 1,
    commandService: null,
    timeoutLimit: 5000
};
/**
 * wrapper function of queries
 * @param {Object} commandOptions
 * @param {Object} transactions
 */
function command(_a, tx) {
    var _b = _a === void 0 ? DEFAULT_OPTIONS : _a, privateKeys = _b.privateKeys, creatorAccountId = _b.creatorAccountId, quorum = _b.quorum, commandService = _b.commandService, timeoutLimit = _b.timeoutLimit;
    var txToSend = txHelper_1["default"].addMeta(tx, {
        creatorAccountId: creatorAccountId,
        quorum: quorum
    });
    txToSend = util_1.signWithArrayOfKeys(txToSend, privateKeys);
    var txClient = commandService;
    return util_1.sendTransactions([txToSend], txClient, timeoutLimit);
}
/**
 * addAssetQuantity
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.assetId
 * @property {Number} params.amount
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#add-asset-quantity
 */
function addAssetQuantity(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'addAssetQuantity', validation_1["default"](params, ['assetId', 'amount'])));
}
/**
 * addPeer
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.address
 * @property {String} params.peerKey
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#add-peer
 */
function addPeer(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'addPeer', {
        peer: validation_1["default"](params, ['address', 'peerKey'])
    }));
}
/**
 * addSignatory
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.publicKey
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#add-signatory
 */
function addSignatory(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'addSignatory', validation_1["default"](params, ['accountId', 'publicKey'])));
}
/**
 * appendRole
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.roleName
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#append-role
 */
function appendRole(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'appendRole', validation_1["default"](params, ['accountId', 'roleName'])));
}
/**
 * callEngine
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.type
 * @property {String} params.caller
 * @property {String} params.callee
 * @property {String} params.input
 * @link //https://iroha.readthedocs.io/en/master/develop/api/commands.html#call-engine
 */
function callEngine(commandOptions, _a) {
    var _b = _a.type, type = _b === void 0 ? commands_pb_1.CallEngine.EngineType.KSOLIDITY : _b, caller = _a.caller, callee = _a.callee, input = _a.input;
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'callEngine', {
        type: type,
        caller: caller,
        callee: callee,
        input: input
    }));
}
/**
 * compareAndSetAccountDetail
 * @param {Object} commandOptions
 * @param {Object} args
 * @property {String} args.accountId
 * @property {String} args.key
 * @property {String} args.value
 * @property {String} args.oldValue
 * @property {boolean} args.checkEmpty
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#compare-and-set-account-detail
 */
function compareAndSetAccountDetail(commandOptions, _a) {
    var accountId = _a.accountId, key = _a.key, value = _a.value, oldValue = _a.oldValue, checkEmpty = _a.checkEmpty;
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'compareAndSetAccountDetail', {
        accountId: accountId,
        key: key,
        value: value,
        oldValue: oldValue,
        checkEmpty: checkEmpty
    }));
}
/**
 * createAccount
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountName
 * @property {String} params.domainId
 * @property {String} params.publicKey
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#create-account
 */
function createAccount(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'createAccount', validation_1["default"](params, ['accountName', 'domainId', 'publicKey'])));
}
/**
 * createAsset
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.assetName
 * @property {String} params.domainId
 * @property {Number} params.precision
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#create-asset
 */
function createAsset(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'createAsset', validation_1["default"](params, ['assetName', 'domainId', 'precision'])));
}
/**
 * createDomain
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.domainId
 * @property {String} params.defaultRole
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#create-domain
 */
function createDomain(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'createDomain', validation_1["default"](params, ['domainId', 'defaultRole'])));
}
/**
 * createRole
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.roleName
 * @property {Number[]} params.permissionsList
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#create-role
 */
function createRole(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'createRole', validation_1["default"](params, ['roleName', 'permissionsList'])));
}
/**
 * detachRole
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.roleName
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#detach-role
 */
function detachRole(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'detachRole', validation_1["default"](params, ['accountId', 'roleName'])));
}
/**
 * grantPermission
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.permission
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#grant-permission
 */
function grantPermission(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'grantPermission', validation_1["default"](params, ['accountId', 'permission'])));
}
/**
 * removeSignatory
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.publicKey
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#remove-signatory
 */
function removeSignatory(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'removeSignatory', validation_1["default"](params, ['accountId', 'publicKey'])));
}
/**
 * revokePermission
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.permission
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#revoke-permission
 */
function revokePermission(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'revokePermission', validation_1["default"](params, ['accountId', 'permission'])));
}
/**
 * setAccountDetail
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.key
 * @property {String} params.value
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#set-account-detail
 */
function setAccountDetail(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'setAccountDetail', validation_1["default"](params, ['accountId', 'key', 'value'])));
}
/**
 * setAccountQuorum
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {Number} params.quorum
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#set-account-quorum
 */
function setAccountQuorum(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'setAccountQuorum', validation_1["default"](params, ['accountId', 'quorum'])));
}
/**
 * setSettingValue
 * This command is not available for use, it was added for backward compatibility with Iroha
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.key
 * @property {String} params.value
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#set-setting-value
 */
function setSettingValue(commandOptions, params) {
    throw new Error('Command not allowed to use');
    // return command(
    //   commandOptions,
    //   txHelper.addCommand(
    //     txHelper.emptyTransaction(),
    //     'setSettingValue',
    //     validate(params, ['key', 'value'])
    //   )
    // )
}
/**
 * subtractAssetQuantity
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.assetId
 * @property {Number} params.amount
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#subtract-asset-quantity
 */
function subtractAssetQuantity(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'subtractAssetQuantity', validation_1["default"](params, ['assetId', 'amount'])));
}
/**
 * transferAsset
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.srcAccountId
 * @property {String} params.destAccountId
 * @property {String} params.assetId
 * @property {String} params.description
 * @property {Number} params.amount
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#transfer-asset
 */
function transferAsset(commandOptions, params) {
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'transferAsset', validation_1["default"](params, ['srcAccountId', 'destAccountId', 'assetId', 'description', 'amount'])));
}
/**
 * removePeer
 * @param {Object} commandOptions
 * @param {Object} args
 * @property {String} args.publicKey
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#remove-peer
 */
function removePeer(commandOptions, _a) {
    var publicKey = _a.publicKey;
    return command(commandOptions, txHelper_1["default"].addCommand(txHelper_1["default"].emptyTransaction(), 'removePeer', {
        publicKey: publicKey
    }));
}
exports["default"] = {
    addAssetQuantity: addAssetQuantity,
    addPeer: addPeer,
    addSignatory: addSignatory,
    appendRole: appendRole,
    compareAndSetAccountDetail: compareAndSetAccountDetail,
    callEngine: callEngine,
    createAccount: createAccount,
    createAsset: createAsset,
    createDomain: createDomain,
    createRole: createRole,
    detachRole: detachRole,
    grantPermission: grantPermission,
    removePeer: removePeer,
    removeSignatory: removeSignatory,
    revokePermission: revokePermission,
    setAccountDetail: setAccountDetail,
    setAccountQuorum: setAccountQuorum,
    setSettingValue: setSettingValue,
    subtractAssetQuantity: subtractAssetQuantity,
    transferAsset: transferAsset
};
//# sourceMappingURL=index.js.map