import * as Transaction from './proto/transaction_pb';
import { AddSignatory, TransferAsset, AddAssetQuantity, CreateAsset, RemoveSignatory, SetAccountQuorum, DetachRole, GrantPermission, RevokePermission, AddPeer, CreateAccount, SetAccountDetail, CreateDomain, AppendRole, CreateRole, SubtractAssetQuantity, CompareAndSetAccountDetail, RemovePeer, CallEngine } from './proto/commands_pb';
declare class Chain {
    txs: Transaction.Transaction[];
    constructor(txs: Transaction.Transaction[]);
    sign(privateKeys: any, transactionId: any): Chain;
    send(commandService: any, timeoutLimit?: number, statusesList?: any[]): Promise<unknown>;
}
declare class TxBuilder {
    tx: Transaction.Transaction;
    constructor(tx?: Transaction.Transaction);
    addAssetQuantity(params: AddAssetQuantity.AsObject): TxBuilder;
    addPeer(params: AddPeer.AsObject): TxBuilder;
    addSignatory(params: AddSignatory.AsObject): TxBuilder;
    callEngine(params: CallEngine.AsObject): TxBuilder;
    createAsset(params: CreateAsset.AsObject): TxBuilder;
    createAccount(params: CreateAccount.AsObject): TxBuilder;
    setAccountDetail(params: SetAccountDetail.AsObject): TxBuilder;
    createDomain(params: CreateDomain.AsObject): TxBuilder;
    removeSignatory(params: RemoveSignatory.AsObject): TxBuilder;
    setAccountQuorum(params: SetAccountQuorum.AsObject): TxBuilder;
    transferAsset(params: TransferAsset.AsObject): TxBuilder;
    appendRole(params: AppendRole.AsObject): TxBuilder;
    detachRole(params: DetachRole.AsObject): TxBuilder;
    createRole(params: CreateRole.AsObject): TxBuilder;
    grantPermission(params: GrantPermission.AsObject): TxBuilder;
    revokePermission(params: RevokePermission.AsObject): TxBuilder;
    subtractAssetQuantity(params: SubtractAssetQuantity.AsObject): TxBuilder;
    compareAndSetAccountDetail(params: CompareAndSetAccountDetail.AsObject): TxBuilder;
    setSettingValue(): void;
    removePeer(params: RemovePeer.AsObject): TxBuilder;
    addMeta(creatorAccountId: string, quorum: number): TxBuilder;
    sign(privateKeys: any): TxBuilder;
    send(commandService: any, timeoutLimit?: number, statusesList?: any[]): Promise<unknown>;
}
declare class BatchBuilder {
    txs: Transaction.Transaction[];
    constructor(txs: Transaction.Transaction[]);
    addTransaction(tx: Transaction.Transaction): BatchBuilder;
    /**
     * 0 - ATOMIC
     * 1 - ORDERED
     */
    setBatchMeta(type: number): Chain;
}
export { TxBuilder, BatchBuilder };
