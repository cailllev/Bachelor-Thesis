"use strict";
exports.__esModule = true;
var assetIdDelimiter = '#';
var accountIdDelimiter = '@';
var accountDetailsKeyPattern = /^[A-Za-z0-9_]{1,64}$/;
var accountDetailsValueLenght = 4096;
var accountPattern = /^[a-z_0-9]{1,32}$/;
var domainPattern = /^([a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$/;
var roleNamePattern = /^[a-z_0-9]{1,32}$/;
var assetNamePattern = /^[a-z_0-9]{1,32}$/;
var hexString = /^[0-9a-fA-F]*$/;
function checkHex(value) {
    if (!hexString.test(value)) {
        return {
            isValid: false,
            reason: "Hex should match " + hexString
        };
    }
    return { isValid: true };
}
function checkAmount(amount) {
    var formattedAmount = Number(amount);
    if (!Number.isFinite(formattedAmount)) {
        return {
            isValid: false,
            reason: 'Amount should be a number'
        };
    }
    if (formattedAmount < 0) {
        return {
            isValid: false,
            reason: 'Amount should be positive'
        };
    }
    if (formattedAmount > Number.MAX_SAFE_INTEGER) {
        return {
            isValid: false,
            reason: 'Amount does not fit into MAX_SAFE_INTEGER'
        };
    }
    return { isValid: true };
}
function checkPresission(precision) {
    if (precision < 0 || precision > 255) {
        return {
            isValid: false,
            reason: 'Precision should be 0 <= precision <= 255'
        };
    }
    return { isValid: true };
}
function checkAccountName(accountName) {
    if (!accountPattern.test(accountName)) {
        return {
            isValid: false,
            reason: "Account name should match " + accountPattern
        };
    }
    return { isValid: true };
}
function checkAssetName(assetName) {
    if (!assetNamePattern.test(assetName)) {
        return {
            isValid: false,
            reason: "Asset name should match " + assetNamePattern
        };
    }
    return { isValid: true };
}
function checkDomain(domain) {
    if (!domainPattern.test(domain)) {
        return {
            isValid: false,
            reason: "Domain should match " + domainPattern
        };
    }
    return { isValid: true };
}
function checkAccountId(accountId) {
    var parts = accountId.split(accountIdDelimiter);
    if (parts.length !== 2) {
        return {
            isValid: false,
            reason: 'Account ID should match account@domain'
        };
    }
    var vName = checkAccountName(parts[0]);
    var vDomain = checkDomain(parts[1]);
    if (!vName.isValid) {
        return vName;
    }
    if (!vDomain.isValid) {
        return vDomain;
    }
    return { isValid: true };
}
function checkAssetId(assetId) {
    var parts = assetId.split(assetIdDelimiter);
    if (parts.length !== 2) {
        return {
            isValid: false,
            reason: 'Asset ID should match asset#domain'
        };
    }
    var vName = checkAssetName(parts[0]);
    var vDomain = checkDomain(parts[1]);
    if (!vName.isValid) {
        return vName;
    }
    if (!vDomain.isValid) {
        return vDomain;
    }
    return { isValid: true };
}
function checkDescription(description) {
    if (description.length > 64) {
        return {
            isValid: false,
            reason: 'Description length should be smaller then 64 symbols'
        };
    }
    return { isValid: true };
}
function checkQuorum(quorum) {
    if (quorum < 0 || quorum > 128) {
        return {
            isValid: false,
            reason: 'Quorum should be 0 < quorum <= 128'
        };
    }
    return { isValid: true };
}
function checkRoleName(name) {
    if (!roleNamePattern.test(name)) {
        return {
            isValid: false,
            reason: "Role name should match " + roleNamePattern
        };
    }
    return { isValid: true };
}
function checkAccountDetailsKey(key) {
    if (!accountDetailsKeyPattern.test(key)) {
        return {
            isValid: false,
            reason: "Key should match " + accountDetailsKeyPattern
        };
    }
    return { isValid: true };
}
function checkAccountDetailsValue(value) {
    if (value.length > accountDetailsValueLenght) {
        return {
            isValid: false,
            reason: "Value length should be smaller then " + accountDetailsValueLenght
        };
    }
    return { isValid: true };
}
function toImplement() {
    return { isValid: true };
}
exports["default"] = {
    checkHex: checkHex,
    checkAmount: checkAmount,
    checkPresission: checkPresission,
    checkAccountName: checkAccountName,
    checkAssetName: checkAssetName,
    checkDomain: checkDomain,
    checkAccountId: checkAccountId,
    checkAssetId: checkAssetId,
    checkDescription: checkDescription,
    checkQuorum: checkQuorum,
    checkRoleName: checkRoleName,
    checkAccountDetailsKey: checkAccountDetailsKey,
    checkAccountDetailsValue: checkAccountDetailsValue,
    toImplement: toImplement
};
//# sourceMappingURL=checks.js.map