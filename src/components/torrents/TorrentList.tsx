import * as React from 'react';
import { connect } from 'react-redux';

import Store from '../../store';
import TorrentRow from './TorrentRow';
import ITorrent from '../../models/ITorrent';

export type Props = {
    torrents: ITorrent[];
};

type ConnectedState = {};
type ConnectedDispatch = {};

type CombinedProps = Props & ConnectedDispatch & ConnectedState;
class TorrentListComponent extends React.Component<CombinedProps> {
    public render() {
        const torrents = this.props.torrents;
        const rows = torrents.map((torrent: ITorrent) => {
            return (<TorrentRow torrent={torrent} key={torrent.id} />);
        });
        return (
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
        );
    }
}

const TorrentList: React.ComponentClass<Props> =
    connect()(TorrentListComponent);
export default TorrentList;
