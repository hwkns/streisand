import * as React from 'react';
import { Link } from 'react-router';

import ForumPostCell from './ForumPostCell';
import { IPartialForumTopic } from '../../models/forums/IForumTopic';

export type Props = {
    topic: IPartialForumTopic;
};

export default function ForumTopicRow(props: Props) {
    const topic = props.topic;
    return (
        <tr>
            <td>
                <Link to={'/topic/' + topic.id} title={topic.title}>{topic.title}</Link>
            </td>
            <ForumPostCell id={topic.latestPost} />
            <td>{topic.numberOfThreads}</td>
            <td>{topic.numberOfPosts}</td>
        </tr>
    );
}