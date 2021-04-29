/// <reference types="node" />
declare enum CryptoAlgorithms {
    ed25519sha2 = 0,
    ed25519sha3 = 1
}
declare class Crypto {
    private algorithm;
    getAlgorithm(): CryptoAlgorithms;
    setAlgorithm(algorithm: CryptoAlgorithms): void;
}
declare const _default: {
    CryptoAlgorithms: typeof CryptoAlgorithms;
    libraryCrypto: Crypto;
    generateKeyPair: () => {
        publicKey: string;
        privateKey: string;
    };
    derivePublicKey: (privateKeyHex: string) => Buffer;
    sign: (payload: Buffer, publicKey: Buffer, privateKey: Buffer) => Buffer;
};
export default _default;
