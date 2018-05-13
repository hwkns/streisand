import * as React from 'react';
import * as redux from 'redux';
import { connect } from 'react-redux';

import Store from '../../store';
import IUser from '../../models/IUser';
import { getItem } from '../../utilities/mapping';
import Editor, { IEditorHandle } from '../bbcode/Editor';
import { IForumThread } from '../../models/forums/IForumThread';
import { IForumPostUpdate } from '../../models/forums/IForumPost';
import { postReply } from '../../actions/forums/posts/CreatePostAction';

export type Props = {
    thread: IForumThread;
};

type ConnectedState = {
    author?: IUser;
};

type ConnectedDispatch = {
    postReply: (post: IForumPostUpdate) => void;
};

type CombinedProps = Props & ConnectedDispatch & ConnectedState;
class ForumReplyComponent extends React.Component<CombinedProps> {
    private _editorHandle: IEditorHandle;

    public render() {
        const onHandle = (handle: IEditorHandle) => { this._editorHandle = handle; };
        const onSave = () => {
            const content = this._editorHandle.getContent();
            this.props.postReply({
                thread: this.props.thread.id,
                body: content
            });
        };
        return (
            <div className="panel panel-primary">
                <div className="panel-heading" >
                    Post your reply
                </div>
                <div className="panel-body">
                    <Editor content={''} size="small" receiveHandle={onHandle} />
                </div>
                <div className="panel-footer">
                    <div className=" btn-toolbar" style={{ display: 'flex', flexFlow: 'row-reverse' }}>
                        <button type="button" className="btn btn-sm btn-primary" onClick={onSave}>
                            Post reply
                        </button>
                    </div>
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state: Store.All, ownProps: Props): ConnectedState => {
    return {
        author: getItem({
            id: state.sealed.currentUser.id,
            byId: state.sealed.users.byId
        })
    };
};

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    postReply: (post: IForumPostUpdate) => dispatch(postReply(post))
});

const ForumReply: React.ComponentClass<Props> =
    connect(mapStateToProps, mapDispatchToProps)(ForumReplyComponent);
export default ForumReply;