import IForumPostResponse from './IForumPost';

export interface IForumThreadResponse {
    id: number;
    topic: number;
    topicTitle: string;
    title: string;
    createdAt: string; // Date
    createdBy: string;
    isLocked: boolean;
    isSticky: boolean;
    numberOfPosts: number;
    latestPost: number;
    latestPostAuthor: string;
    posts: IForumPostResponse[];
}

export interface IPartialForumThread {
    id: number;
    title: string;
}

export interface IForumThread extends IPartialForumThread {
    topic: number;
    createdAt: string; // Date
    createdBy: number;
    isLocked: boolean;
    isSticky: boolean;
    numberOfPosts: number;
    latestPost: number;
    latestPostAuthor: number;
    posts: number[];
}
