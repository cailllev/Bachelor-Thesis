/// <reference types="node" />
import { TxList } from './proto/endpoint_pb';
import * as Transaction from './proto/transaction_pb';
declare const _default: {
    addCommand: (transaction: any, commandName: any, params: any) => any;
    addMeta: (transaction: any, { creatorAccountId, createdTime, quorum }: {
        creatorAccountId: any;
        createdTime?: number;
        quorum?: number;
    }) => any;
    sign: (transaction: any, privateKeyHex: any) => any;
    emptyTransaction: () => Transaction.Transaction;
    hash: (transaction: any) => Buffer;
    addBatchMeta: (transactions: any, type: any) => any;
    createTxListFromArray: (transactions: any) => TxList;
};
export default _default;
