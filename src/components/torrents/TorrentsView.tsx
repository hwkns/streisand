import * as React from 'react';
import { connect } from 'react-redux';

import Pager from '../Pager';
import Empty from '../Empty';
import Store from '../../store';
import TorrentRow from './TorrentRow';
import ITorrent from '../../models/ITorrent';

export type Props = {
    page: number;
};

type ConnectedState = {
    total: number;
    torrents: ITorrent[];
    loading: boolean;
};
type ConnectedDispatch = {};

type CombinedProps = Props & ConnectedDispatch & ConnectedState;
class TorrentsViewComponent extends React.Component<CombinedProps> {
    public render() {
        const torrents = this.props.torrents;
        if (!torrents.length) {
            return <Empty loading={this.props.loading} />;
        }
        const rows = torrents.map((torrent: ITorrent) => {
            return (<TorrentRow torrent={torrent} key={torrent.id} />);
        });
        return (
            <div className="bs-component">
                <Pager uri="/torrents" total={this.props.total} page={this.props.page} />
                <table className="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Release Name</th>
                            <th>Resolution</th>
                            <th>Source</th>
                            <th>Size</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
                <Pager uri="/torrents" total={this.props.total} page={this.props.page} />
            </div>
        );
    }
}

const mapStateToProps = (state: Store.All, ownProps: Props): ConnectedState => {
    const page = state.torrents.pages[ownProps.page];
    return {
        total: state.torrents.count,
        loading: page ? page.loading : false,
        torrents: page ? page.items : []
    };
};

const TorrentsView: React.ComponentClass<Props> =
    connect(mapStateToProps)(TorrentsViewComponent);
export default TorrentsView;
