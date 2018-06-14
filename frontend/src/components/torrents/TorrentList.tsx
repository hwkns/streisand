import * as React from 'react';
import {Table} from 'reactstrap';
import {Link} from 'react-router';

import ITorrent from '../../models/ITorrent';
import { getSize } from '../../utilities/dataSize';

export type Props = {
    torrents: ITorrent[];
};

export default function TorrentList(props: Props) {
    const torrents = props.torrents;
    const rows = torrents.map((torrent: ITorrent) => {
        return (<TorrentRow torrent={torrent} key={torrent.id}/>);
    });

    return (
        <Table className="table-borderless" striped hover>
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
        </Table>
    );
}

function TorrentRow(props: { torrent: ITorrent }) {
    const torrent = props.torrent;
    if (!torrent.release) {
        return (
            <Table className="allign-middle" striped hover>
                <thead>
                <tr>
                    <td>No release is tied to this torrent</td>
                </tr>
                </thead>
            </Table>
        );
    }
    const name = torrent.release.releaseName || '<Uknown>';
    const url = `/film/${torrent.release.film.id}/${torrent.id}`;

    const size = getSize(torrent.totalSizeInBytes);
    return (
        <tr>
            <td className="align-middle">
                <Link to={url} title={name}>{name}</Link>
            </td>
            <td className="align-middle">{torrent.release.resolution}</td>
            <td className="align-middle">{torrent.release.sourceMedia}</td>
            <td className="align-middle">{size}</td>
        </tr>
    );
}
