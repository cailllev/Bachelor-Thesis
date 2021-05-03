"use strict";
exports.__esModule = true;
var tslib_1 = require("tslib");
var buffer_1 = require("buffer");
var ed25519sha3 = tslib_1.__importStar(require("ed25519.js"));
var tweetnacl_1 = tslib_1.__importDefault(require("tweetnacl"));
var CryptoAlgorithms;
(function (CryptoAlgorithms) {
    CryptoAlgorithms[CryptoAlgorithms["ed25519sha2"] = 0] = "ed25519sha2";
    CryptoAlgorithms[CryptoAlgorithms["ed25519sha3"] = 1] = "ed25519sha3";
})(CryptoAlgorithms || (CryptoAlgorithms = {}));
var Crypto = /** @class */ (function () {
    function Crypto() {
        this.algorithm = CryptoAlgorithms.ed25519sha3;
    }
    Crypto.prototype.getAlgorithm = function () {
        return this.algorithm;
    };
    Crypto.prototype.setAlgorithm = function (algorithm) {
        this.algorithm = algorithm;
    };
    return Crypto;
}());
var libraryCrypto = new Crypto();
/**
 * Returns a new ed25519-sha3 / ed25519-sha2 keypair
 * Depends on crypto algorithm
 */
var generateKeyPair = function () {
    var type = libraryCrypto.getAlgorithm();
    var keys, publicKey, privateKey;
    if (type === CryptoAlgorithms.ed25519sha3) {
        keys = ed25519sha3.createKeyPair();
        publicKey = (keys.publicKey).toString('hex');
        privateKey = (keys.privateKey).toString('hex');
    }
    else if (type === CryptoAlgorithms.ed25519sha2) {
        keys = tweetnacl_1["default"].sign.keyPair();
        publicKey = buffer_1.Buffer.from(keys.publicKey).toString('hex');
        privateKey = buffer_1.Buffer.from(keys.privateKey).toString('hex');
    }
    else {
        throw new Error('Unsupported crypto algorithm!');
    }
    return { publicKey: publicKey, privateKey: privateKey };
};
var derivePublicKey = function (privateKeyHex) {
    var type = libraryCrypto.getAlgorithm();
    if (type === CryptoAlgorithms.ed25519sha3) {
        return ed25519sha3.derivePublicKey(buffer_1.Buffer.from(privateKeyHex, 'hex'));
    }
    else if (type === CryptoAlgorithms.ed25519sha2) {
        var keyPair = tweetnacl_1["default"].sign.keyPair.fromSecretKey(buffer_1.Buffer.from(privateKeyHex, 'hex'));
        var publicKeyHex = buffer_1.Buffer.from(keyPair.publicKey).toString('hex');
        return buffer_1.Buffer.from("ed0120" + publicKeyHex, 'hex');
    }
    else {
        throw new Error('Unsupported crypto algorithm!');
    }
};
var sign = function (payload, publicKey, privateKey) {
    var type = libraryCrypto.getAlgorithm();
    if (type === CryptoAlgorithms.ed25519sha3) {
        return ed25519sha3.sign(payload, publicKey, privateKey);
    }
    else if (type === CryptoAlgorithms.ed25519sha2) {
        return Buffer.from(tweetnacl_1["default"].sign(payload, privateKey));
    }
    else {
        throw new Error('Unsupported crypto algorithm!');
    }
};
exports["default"] = {
    CryptoAlgorithms: CryptoAlgorithms,
    libraryCrypto: libraryCrypto,
    generateKeyPair: generateKeyPair,
    derivePublicKey: derivePublicKey,
    sign: sign
};
//# sourceMappingURL=cryptoHelper.js.map