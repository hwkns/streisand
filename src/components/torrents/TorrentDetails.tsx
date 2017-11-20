import * as React from 'react';
import { Parser } from 'bbcode-to-react';
import { Tabs, Tab } from 'react-bootstrap';

import IFilm from '../../models/IFilm';
import ITorrent from '../../models/ITorrent';

const parser = new Parser();

export type Props = {
    film: IFilm;
    torrent: ITorrent;
};

export default function TorrentDetails(props: Props) {
    const torrent = props.torrent;
    return (
        <Tabs defaultActiveKey={2}>
            <Tab eventKey={1} title="General"><GeneralContent torrent={torrent} /></Tab>
            <Tab eventKey={2} title="Video"><MediaContent torrent={torrent} /></Tab>
            <Tab eventKey={3} title="Torrent"><TorrentContent torrent={torrent} /></Tab>
        </Tabs>
    );
}

interface IRowProps {
    label: string;
    value: string | number;
}

function InfoRow(props: IRowProps) {
    return (
        <li className="list-group-item">
            <strong>{props.label}</strong>: <span className="text-muted">{props.value}</span>
        </li>
    );
}

function GeneralContent(props: { torrent: ITorrent }) {
    return (
        <div style={{ 'margin-top': '8px' }}>
            <div>{parser.toReact(props.torrent.description)}</div>
        </div>
    );
}

function TorrentContent(props: { torrent: ITorrent }) {
    const torrent = props.torrent;
    return (
        <ul className="list-group" style={{ 'margin-top': '8px' }}>
            <InfoRow label="Release name" value={torrent.releaseName} />
            <InfoRow label="Release group" value={torrent.releaseGroup} />
            <InfoRow label="Uploaded at" value={torrent.uploadedAt} />
            <InfoRow label="Uploaded by" value={torrent.uploadedBy} />
        </ul>
    );
}

function MediaContent(props: { torrent: ITorrent }) {
    const torrent = props.torrent;
    const info = torrent.mediainfo;
    return (
        <ul className="list-group" style={{ 'margin-top': '8px' }}>
            <InfoRow label="Runtime" value={info.runtime} />
            <InfoRow label="Codec" value={torrent.codec} />
            <InfoRow label="Container" value={torrent.container} />
            <InfoRow label="Cut" value={torrent.cut} />
            <InfoRow label="Bite rate" value={info.bitRate} />
            <InfoRow label="Frame rate" value={info.frameRate} />
            <InfoRow label="Source" value={torrent.sourceMedia} />
            <InfoRow label="Aspect ratio" value={info.displayAspectRatio} />
            <InfoRow label="Resolution" value={torrent.resolution} />
            <InfoRow label="Width" value={info.resolutionWidth} />
            <InfoRow label="Height" value={info.resolutionHeight} />
        </ul>
    );
}