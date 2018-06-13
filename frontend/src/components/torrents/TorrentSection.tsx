import * as React from 'react';
import { Table } from 'reactstrap';
import { Link } from 'react-router';

import ITorrent from '../../models/ITorrent';

export type Props = {
    torrents: ITorrent[];
};

export default function TorrentSection(props: Props) {
    const torrents = props.torrents;
    const rows = torrents.map((torrent: ITorrent) => {
        return (<TorrentRow torrent={torrent} key={torrent.id} />);
    });

    return (
        <Table className="table-borderless" striped hover>
            <thead>
                <tr>
                    <th></th>
                    <th>Size</th>
                    <th>Snatched</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </Table>
    );
}

function TorrentRow(props: { torrent: ITorrent }) {
    const torrent = props.torrent;
    if (!torrent.release) {
        return <div style={{ marginTop: '8px' }}>Release is not tied to a torrent.</div>;
    }
    const url = `/film/${torrent.release.film.id}/${torrent.id}`;

    let name = `${torrent.release.codec} / ${torrent.release.container} / ${torrent.release.sourceMedia} / ${torrent.release.resolution}`;
    if (!name) {
        return <tbody style={{ marginTop: '8px' }}>Release is not tied to a torrent.</tbody>;
    }
    if (torrent.release.isScene) {
        name += ' / Scene';
    }

    return (
        <tr>
            <td className="align-middle">
                <Link to={url} title={name}>{name}</Link>
            </td>
            <td className="align-middle">{torrent.file.sizeInBytes}</td>
            <td className="align-middle">{torrent.snatchCount}</td>
        </tr>
    );
}
