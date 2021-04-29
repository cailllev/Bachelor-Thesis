/**
 * Capitalizes string
 * @param {String} string
 * @returns {String} capitalized string
 */
declare const capitalize: (string: any) => any;
declare function reverseEnum<T>(e: T): {
    [value: number]: keyof T;
};
declare function sendTransactions(txs: any, txClient: any, timeoutLimit: any, requiredStatusesStr?: string[]): Promise<unknown>;
declare function signWithArrayOfKeys(tx: any, privateKeys: any): any;
export { capitalize, reverseEnum, sendTransactions, signWithArrayOfKeys };
