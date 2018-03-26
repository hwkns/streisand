
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

export interface IPartialForumPost {
    id: number;
    author: number;
    thread: number;
}

export interface IForumPost extends IPartialForumPost {
    body: string;
    bodyHtml: string;
    createdAt: string; // Date
    modifiedAt: string; // Date
}

export default IForumPost;