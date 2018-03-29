import * as React from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';

import Store from '../../store';
import IUser from '../../models/IUser';
import ForumPostCell from './ForumPostCell';
import IForumThread from '../../models/forums/IForumThread';

export type Props = {
    thread: IForumThread;
};

type ConnectedState = {
    author: IUser;
};
type ConnectedDispatch = {};

type CombinedProps = Props & ConnectedDispatch & ConnectedState;
class ForumThreadRowComponent extends React.Component<CombinedProps> {
    public render() {
        const thread = this.props.thread;
        const author = this.props.author;
        const authorLink = <Link to={'/user/' + author.id} title={author.username}>{author.username}</Link>;
        return (
            <tr>
                <ForumPostCell id={thread.latestPost} />
                <td>{thread.numberOfPosts}</td>
                <td>{authorLink}</td>
            </tr>
        );
    }
}

const mapStateToProps = (state: Store.All, ownProps: Props): ConnectedState => {
    const author = ownProps.thread && state.users.byId[ownProps.thread.createdBy] as IUser;
    return {
        author: author
    };
};

const ForumThreadRow: React.ComponentClass<Props> =
    connect(mapStateToProps)(ForumThreadRowComponent);
export default ForumThreadRow;