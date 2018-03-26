import IPagedResponse from '../../models/base/IPagedResponse';
import { IForumGroupResponse, IForumGroupData } from '../../models/forums/IForumGroup';

export function transformGroups(response: IPagedResponse<IForumGroupResponse>): IForumGroupData {
    const result: IForumGroupData = {
        groups: [],
        topics: [],
        threads: [],
        posts: [],
        users: []
    };

    for (const group of response.results) {
        const transformedGroup = {
            id: group.id,
            title: group.name,
            topics: []
        };
        result.groups.push(transformedGroup);
        for (const topic of group.topics_Data) {
            transformedGroup.topics.push(topic.id);
            result.topics.push({
                id: topic.id,
                title: topic.name,
                group: group.id,
                description: topic.description,
                numberOfThreads: topic.numberOfThreads,
                numberOfPosts: topic.numberOfPosts,
                latestPost: topic.latestPostId
            });

            result.threads.push({
                id: topic.latestPostThreadId,
                title: topic.latestPostThreadTitle
            });

            result.posts.push({
                id: topic.latestPostId,
                thread: topic.latestPostThreadId,
                author: topic.latestPostAuthorId
            });

            result.users.push({
                id: topic.latestPostAuthorId,
                username: topic.latestPostAuthorName
            });
        }
    }

    return result;
}