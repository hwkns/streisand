import { IPartialUser } from '../IUser';
import { IPartialForumPost } from './IForumPost';
import { IPartialForumThread } from './IForumThread';
import { IForumTopicResponse, IPartialForumTopic } from './IForumTopic';

export interface IForumGroupResponse {
    id: number;
    name: string;
    sortOrder: number;
    topicCount: number;
    topics_Data: IForumTopicResponse[];
}

export interface IForumGroup {
    id: number;
    title: string;
    topics: number[];
}

export interface IForumGroupData {
    groups: IForumGroup[];
    topics: IPartialForumTopic[];
    threads: IPartialForumThread[];
    posts: IPartialForumPost[];
    users: IPartialUser[];
}

export default IForumGroup;