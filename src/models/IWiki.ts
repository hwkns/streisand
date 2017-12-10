
// editable fields
export interface IWikiUpdate {
    title: string;
    body: string;
}

interface IWiki extends IWikiUpdate {
    id: number;
    modifiedAt: string; // Date
    createdBy: number; // user id
    modifiedBy: number; // user id
    readAccessMinimumUserClass: number;
    writeAccessMinimumUserClass: number;
}

export default IWiki;