
export interface IForumTopicResponse {
    id: number;
    sortOrder: number;
    name: string;
    description: string;
    minimumUserClass: number;
    numberOfThreads: number;
    numberOfPosts: number;
    latestPostId: number;
    latestPostCreatedAt: string; // Date
    latestPostAuthorId: number;
    latestPostAuthorName: string;
    latestPostThreadId: number;
    latestPostThreadTitle: string;
}

export interface IForumTopic {
    id: number;
    group: number;
    title: string;
    description?: string;
    numberOfThreads?: number;
    numberOfPosts?: number;
    latestPost?: number;
    threads?: number[];
}

export default IForumTopic;