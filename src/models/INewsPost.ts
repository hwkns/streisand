import IUser from './IUser';

interface INewsPost {
    id: number;
    author: IUser;
    thread: {
        id: number,
        title: string;
    };
    body: string;
    bodyHtml: string;
    createdAt: string;
    modifiedAt: string;
}

export default INewsPost;