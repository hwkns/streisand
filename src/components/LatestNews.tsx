import * as React from 'react';
import * as redux from 'redux';
import { connect } from 'react-redux';

import Store from '../store';
import INewsPost from '../models/INewsPost';
import Empty from './Empty';
import { getLatestNews } from '../actions/NewsAction';
import TextView from './bbcode/TextView';
import { getDateDiff } from '../utilities/dates';
import UserLink from './links/UserLink';

export type Props = {};

type ConnectedState = {
    latestNews: INewsPost;
    loading: boolean;
};

type ConnectedDispatch = {
    getLatestNews: () => void;
};

type CombinedProps = ConnectedState & ConnectedDispatch & Props;
class LatestNewsComponent extends React.Component<CombinedProps, void> {
    public componentWillMount() {
        if (!this.props.loading && !this.props.latestNews) {
            this.props.getLatestNews();
        }
    }

    public componentWillReceiveProps(props: CombinedProps) {
        if (!props.loading && !props.latestNews) {
            this.props.getLatestNews();
        }
    }

    public render() {
        const post = this.props.latestNews;
        if (this.props.loading || !post) {
            return <Empty loading={this.props.loading} />;
        }

        const posted = getDateDiff({ past: post.createdAt });

        return (
            <div className="panel panel-default">
                <div className="panel-heading">{post.thread.title} - posted by <UserLink user={post.author} /> { posted }</div>
                <div className="panel-body">
                    <TextView content={post.body} />
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state: Store.All, ownProps: Props): ConnectedState => ({
    loading: state.sealed.news.loading,
    latestNews: state.sealed.news.latest
});

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    getLatestNews: () => dispatch(getLatestNews())
});

const LatestNews: React.ComponentClass<Props> =
    connect(mapStateToProps, mapDispatchToProps)(LatestNewsComponent);
export default LatestNews;
