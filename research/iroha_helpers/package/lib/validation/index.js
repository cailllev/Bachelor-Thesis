"use strict";
exports.__esModule = true;
var tslib_1 = require("tslib");
var lodash_isequal_1 = tslib_1.__importDefault(require("lodash.isequal"));
var lodash_isplainobject_1 = tslib_1.__importDefault(require("lodash.isplainobject"));
var checks_1 = tslib_1.__importDefault(require("./checks"));
var allowEmpty = [
    'key',
    'writer'
];
var schema = {
    amount: checks_1["default"].checkAmount,
    precision: checks_1["default"].checkPresission,
    accountName: checks_1["default"].checkAccountName,
    accountId: checks_1["default"].checkAccountId,
    domainId: checks_1["default"].checkDomain,
    assetId: checks_1["default"].checkAssetId,
    srcAccountId: checks_1["default"].checkAccountId,
    destAccountId: checks_1["default"].checkAccountId,
    description: checks_1["default"].checkDescription,
    quorum: checks_1["default"].checkQuorum,
    assetName: checks_1["default"].checkAssetName,
    roleName: checks_1["default"].checkRoleName,
    defaultRole: checks_1["default"].checkRoleName,
    key: checks_1["default"].checkAccountDetailsKey,
    value: checks_1["default"].checkAccountDetailsValue,
    oldValue: checks_1["default"].checkAccountDetailsValue,
    roleId: checks_1["default"].checkRoleName,
    writer: checks_1["default"].checkAccountId,
    txHash: checks_1["default"].checkHex,
    caller: checks_1["default"].checkAccountId,
    type: checks_1["default"].toImplement,
    callee: checks_1["default"].toImplement,
    input: checks_1["default"].toImplement,
    peerKey: checks_1["default"].toImplement,
    publicKey: checks_1["default"].toImplement,
    permissionsList: checks_1["default"].toImplement,
    permission: checks_1["default"].toImplement,
    txHashesList: checks_1["default"].toImplement,
    address: checks_1["default"].toImplement,
    pageSize: checks_1["default"].toImplement,
    firstTxHash: checks_1["default"].toImplement,
    height: checks_1["default"].toImplement
};
var compare = function (a, b) { return a - b; };
function validateParams(object, required) {
    if (!lodash_isplainobject_1["default"](object)) {
        throw new Error("Expected type of arguments: object, actual: " + typeof object);
    }
    var keysSorted = {
        current: Object.keys(object).sort(compare),
        expected: required.sort(compare)
    };
    var isEquals = lodash_isequal_1["default"](keysSorted.current, keysSorted.expected);
    if (!isEquals) {
        throw new Error("Expected arguments: " + keysSorted.expected + ", actual: " + keysSorted.current);
    }
    var errors = required
        .map(function (property) {
        var validator = schema[property];
        // TODO: Create better way to handle not required arguments
        if (allowEmpty.includes(property)) {
            return [
                property,
                { isValid: true }
            ];
        }
        return [property, validator(object[property])];
    })
        .reduce(function (errors, pair) {
        if (pair[1].isValid === false) {
            errors.push(new Error("Field \"" + pair[0] + "\" (value: \"" + object[pair[0]] + "\") is incorrect\nReason: " + pair[1].reason));
        }
        return errors;
    }, []);
    if (errors.length) {
        throw errors;
    }
    return object;
}
exports["default"] = validateParams;
//# sourceMappingURL=index.js.map