import { IForumGroup } from './IForumGroup';
import { IPage, IPagedItemSet } from '../base/IPagedItemSet';
import { IPartialForumPost, IForumPost } from './IForumPost';
import { IPartialForumThread, IForumThread } from './IForumThread';
import { IPartialForumTopic, IForumTopic } from './IForumTopic';

export type ForumGroupData = IPage<IForumGroup>;
export type ForumTopicData = IPagedItemSet<IPartialForumTopic | IForumTopic>;
export type ForumThreadData = IPagedItemSet<IPartialForumThread | IForumThread>;
export type ForumPostData = IPagedItemSet<IPartialForumPost | IForumPost>;

interface IForumData {
    groups: ForumGroupData;
    topics: ForumTopicData;
    threads: ForumThreadData;
    posts: ForumPostData;
}

export default IForumData;