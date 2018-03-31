import IPagedResponse from '../../models/base/IPagedResponse';
import { IForumPostResponse } from '../../models/forums/IForumPost';
import { IForumThreadResponse } from '../../models/forums/IForumThread';
import { IForumGroupResponse, IForumGroupData} from '../../models/forums/IForumGroup';

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
        for (const topic of group.topicsData) {
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
                title: topic.latestPostThreadTitle,
                topic: topic.id
            });

            result.posts.push({
                id: topic.latestPostId,
                thread: topic.latestPostThreadId,
                author: topic.latestPostAuthorId,
                createdAt: topic.latestPostCreatedAt
            });

            result.users.push({
                id: topic.latestPostAuthorId,
                username: topic.latestPostAuthorName
            });
        }
    }

    return result;
}

export function transformTopic(response: IPagedResponse<IForumThreadResponse>): IForumGroupData {
    const result: IForumGroupData = {
        groups: [],
        topics: [],
        threads: [],
        posts: [],
        users: []
    };

    let addedCommon = false;
    for (const thread of response.results) {
        if (!addedCommon) {
            result.groups.push({
                id: thread.groupId,
                title: thread.groupName
            });
            result.topics.push({
                id: thread.topic,
                title: thread.topicTitle,
                group: thread.groupId
            });
            addedCommon = true;
        }

        result.threads.push({
            id: thread.id,
            title: thread.title,
            topic: thread.topic,
            createdAt: thread.createdAt,
            createdBy: thread.createdById,
            isLocked: thread.isLocked,
            isSticky: thread.isSticky,
            numberOfPosts: thread.numberOfPosts,
            latestPost: thread.latestPost
        });

        result.posts.push({
            id: thread.latestPost,
            thread: thread.id,
            author: thread.latestPostAuthorId,
            createdAt: thread.latestPostCreatedAt
        });

        result.users.push({
            id: thread.createdById,
            username: thread.createdByUsername
        });

        result.users.push({
            id: thread.latestPostAuthorId,
            username: thread.latestPostAuthorUsername
        });
    }

    return result;
}

export function transformThread(response: IPagedResponse<IForumPostResponse>): IForumGroupData {
    const result: IForumGroupData = {
        groups: [],
        topics: [],
        threads: [],
        posts: [],
        users: []
    };

    let addedCommon = false;
    for (const post of response.results) {
        if (!addedCommon) {
            result.topics.push({
                id: post.topicId,
                title: post.topicName
            });
            result.threads.push({
                id: post.thread,
                title: post.threadTitle,
                topic: post.topicId
            });
            addedCommon = true;
        }

        result.posts.push({
            id: post.id,
            thread: post.thread,
            author: 10437, // TODO: fix this when the field gets added to the API
            createdAt: post.createdAt,
            modifiedAt: post.modifiedAt,
            body: post.body
        });

        // post creater
        result.users.push({
            id: 10437, // TODO: fix this when the field gets added to the API
            username: post.author
        });

        // post modifier
        // result.users.push({
        //     id: 10437, // TODO: fix this when the field gets added to the API
        //     username: 'neebs' // TODO: fix this when the field gets added to the API
        // });
    }

    return result;
}