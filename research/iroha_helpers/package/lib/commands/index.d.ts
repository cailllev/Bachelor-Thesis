/**
 * addAssetQuantity
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.assetId
 * @property {Number} params.amount
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#add-asset-quantity
 */
declare function addAssetQuantity(commandOptions: any, params: any): Promise<unknown>;
/**
 * addPeer
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.address
 * @property {String} params.peerKey
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#add-peer
 */
declare function addPeer(commandOptions: any, params: any): Promise<unknown>;
/**
 * addSignatory
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.publicKey
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#add-signatory
 */
declare function addSignatory(commandOptions: any, params: any): Promise<unknown>;
/**
 * appendRole
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.roleName
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#append-role
 */
declare function appendRole(commandOptions: any, params: any): Promise<unknown>;
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
declare function callEngine(commandOptions: any, { type, caller, callee, input }: {
    type?: 0;
    caller: any;
    callee: any;
    input: any;
}): Promise<unknown>;
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
declare function compareAndSetAccountDetail(commandOptions: any, { accountId, key, value, oldValue, checkEmpty }: {
    accountId: any;
    key: any;
    value: any;
    oldValue: any;
    checkEmpty: any;
}): Promise<unknown>;
/**
 * createAccount
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountName
 * @property {String} params.domainId
 * @property {String} params.publicKey
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#create-account
 */
declare function createAccount(commandOptions: any, params: any): Promise<unknown>;
/**
 * createAsset
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.assetName
 * @property {String} params.domainId
 * @property {Number} params.precision
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#create-asset
 */
declare function createAsset(commandOptions: any, params: any): Promise<unknown>;
/**
 * createDomain
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.domainId
 * @property {String} params.defaultRole
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#create-domain
 */
declare function createDomain(commandOptions: any, params: any): Promise<unknown>;
/**
 * createRole
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.roleName
 * @property {Number[]} params.permissionsList
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#create-role
 */
declare function createRole(commandOptions: any, params: any): Promise<unknown>;
/**
 * detachRole
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.roleName
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#detach-role
 */
declare function detachRole(commandOptions: any, params: any): Promise<unknown>;
/**
 * grantPermission
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.permission
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#grant-permission
 */
declare function grantPermission(commandOptions: any, params: any): Promise<unknown>;
/**
 * removeSignatory
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.publicKey
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#remove-signatory
 */
declare function removeSignatory(commandOptions: any, params: any): Promise<unknown>;
/**
 * revokePermission
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.permission
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#revoke-permission
 */
declare function revokePermission(commandOptions: any, params: any): Promise<unknown>;
/**
 * setAccountDetail
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {String} params.key
 * @property {String} params.value
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#set-account-detail
 */
declare function setAccountDetail(commandOptions: any, params: any): Promise<unknown>;
/**
 * setAccountQuorum
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.accountId
 * @property {Number} params.quorum
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#set-account-quorum
 */
declare function setAccountQuorum(commandOptions: any, params: any): Promise<unknown>;
/**
 * setSettingValue
 * This command is not available for use, it was added for backward compatibility with Iroha
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.key
 * @property {String} params.value
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#set-setting-value
 */
declare function setSettingValue(commandOptions: any, params: any): void;
/**
 * subtractAssetQuantity
 * @param {Object} commandOptions
 * @param {Object} params
 * @property {String} params.assetId
 * @property {Number} params.amount
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#subtract-asset-quantity
 */
declare function subtractAssetQuantity(commandOptions: any, params: any): Promise<unknown>;
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
declare function transferAsset(commandOptions: any, params: any): Promise<unknown>;
/**
 * removePeer
 * @param {Object} commandOptions
 * @param {Object} args
 * @property {String} args.publicKey
 * @link https://iroha.readthedocs.io/en/master/develop/api/commands.html#remove-peer
 */
declare function removePeer(commandOptions: any, { publicKey }: {
    publicKey: any;
}): Promise<unknown>;
declare const _default: {
    addAssetQuantity: typeof addAssetQuantity;
    addPeer: typeof addPeer;
    addSignatory: typeof addSignatory;
    appendRole: typeof appendRole;
    compareAndSetAccountDetail: typeof compareAndSetAccountDetail;
    callEngine: typeof callEngine;
    createAccount: typeof createAccount;
    createAsset: typeof createAsset;
    createDomain: typeof createDomain;
    createRole: typeof createRole;
    detachRole: typeof detachRole;
    grantPermission: typeof grantPermission;
    removePeer: typeof removePeer;
    removeSignatory: typeof removeSignatory;
    revokePermission: typeof revokePermission;
    setAccountDetail: typeof setAccountDetail;
    setAccountQuorum: typeof setAccountQuorum;
    setSettingValue: typeof setSettingValue;
    subtractAssetQuantity: typeof subtractAssetQuantity;
    transferAsset: typeof transferAsset;
};
export default _default;
