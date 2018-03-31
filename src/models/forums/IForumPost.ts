
export interface IForumPostResponse {
    id: number;
    thread: number;
    threadTitle: string;
    topicId: number;
    topicName: string;
    author: string;
    body: string;
    bodyHtml: string;
    createdAt: string; // Date
    modifiedAt: string; // Date
}

export interface IForumPost {
    id: number;
    author: number;
    thread: number;
    createdAt: string; // Date
    body?: string;
    modifiedAt?: string; // Date
}

export default IForumPost;