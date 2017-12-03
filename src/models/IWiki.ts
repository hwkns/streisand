
interface IWiki {
    id: number;
    modifiedAt: string; // Date
    createdBy: number; // user id
    modifiedBy: number; // user id
    title: string;
    body: string;
    readAccessMinimumUserClass: number;
    writeAccessMinimumUserClass: number;
}

export default IWiki;