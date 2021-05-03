import * as Queries from './proto/queries_pb';
declare const _default: {
    sign: (query: any, privateKeyHex: any) => any;
    addMeta: (query: any, { creatorAccountId, createdTime, queryCounter }: {
        creatorAccountId: any;
        createdTime?: number;
        queryCounter?: number;
    }) => any;
    addQuery: (query: any, queryName: any, params?: {}) => any;
    emptyQuery: () => Queries.Query;
    emptyBlocksQuery: () => Queries.BlocksQuery;
};
export default _default;
