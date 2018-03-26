import * as React from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';

import Store from '../../store';
import { IPartialUser } from '../../models/IUser';
import { IPartialForumPost } from '../../models/forums/IForumPost';
import { IPartialForumThread } from '../../models/forums/IForumThread';
import { getDateDiff } from '../../utilities/dates';

export type Props = {
    id: number;
};

type ConnectedState = {
    post: IPartialForumPost;
    thread: IPartialForumThread;
    author: IPartialUser;
};
type ConnectedDispatch = {};

type CombinedProps = Props & ConnectedDispatch & ConnectedState;
class ForumPostCellComponent extends React.Component<CombinedProps> {
    public render() {
        // const post = this.props.post;
        const thread = this.props.thread;
        const author = this.props.author;
        const posted = getDateDiff({ past: (new Date()) });
        const authorLink = <Link to={'/user/' + author.id} title={author.username}>{author.username}</Link>;
        const threadLink = <Link to={'/thread/' + thread.id} title={thread.title}>{thread.title}</Link>;
        return (
            <td>
                {authorLink} posted in {threadLink} {posted}
            </td>
        );
    }
}

const mapStateToProps = (state: Store.All, ownProps: Props): ConnectedState => {
    const post = state.forums.posts.byId[ownProps.id] as IPartialForumPost;
    const author = post && { id: 5, username: 'The Dude' };
    const thread = post && state.forums.threads.byId[post.thread];
    return {
        post: post,
        thread: thread as IPartialForumThread,
        author: author as IPartialUser
    };
};

const ForumPostCell: React.ComponentClass<Props> =
    connect(mapStateToProps)(ForumPostCellComponent);
export default ForumPostCell;