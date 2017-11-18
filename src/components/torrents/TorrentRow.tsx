import * as React from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';

import Store from '../../store';
import ITorrent from '../../models/ITorrent';

export type Props = {
    torrent: ITorrent;
};

type CombinedProps = Props;
class TorrentRow extends React.Component<CombinedProps> {
    public render() {
        const torrent = this.props.torrent;
        const name = torrent.releaseName || '<Uknown>';
        return (
            <tr>
                <td>
                    <Link to={'/film/' + torrent.filmId} title={name}>{name}</Link>
                </td>
                <td>{torrent.resolution}</td>
                <td>{torrent.sourceMedia}</td>
                <td>{torrent.size}</td>
            </tr>
        );
    }
}

export default TorrentRow;