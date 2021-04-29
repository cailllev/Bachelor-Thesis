interface ValidationResponse {
    isValid: boolean;
    reason?: string;
}
declare function checkHex(value: any): ValidationResponse;
declare function checkAmount(amount: any): ValidationResponse;
declare function checkPresission(precision: any): ValidationResponse;
declare function checkAccountName(accountName: any): ValidationResponse;
declare function checkAssetName(assetName: any): ValidationResponse;
declare function checkDomain(domain: any): ValidationResponse;
declare function checkAccountId(accountId: any): ValidationResponse;
declare function checkAssetId(assetId: any): ValidationResponse;
declare function checkDescription(description: any): ValidationResponse;
declare function checkQuorum(quorum: any): ValidationResponse;
declare function checkRoleName(name: any): ValidationResponse;
declare function checkAccountDetailsKey(key: any): ValidationResponse;
declare function checkAccountDetailsValue(value: any): ValidationResponse;
declare function toImplement(): ValidationResponse;
declare const _default: {
    checkHex: typeof checkHex;
    checkAmount: typeof checkAmount;
    checkPresission: typeof checkPresission;
    checkAccountName: typeof checkAccountName;
    checkAssetName: typeof checkAssetName;
    checkDomain: typeof checkDomain;
    checkAccountId: typeof checkAccountId;
    checkAssetId: typeof checkAssetId;
    checkDescription: typeof checkDescription;
    checkQuorum: typeof checkQuorum;
    checkRoleName: typeof checkRoleName;
    checkAccountDetailsKey: typeof checkAccountDetailsKey;
    checkAccountDetailsValue: typeof checkAccountDetailsValue;
    toImplement: typeof toImplement;
};
export default _default;
