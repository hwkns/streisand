import * as React from 'react';
import * as redux from 'redux';
import { connect } from 'react-redux';
import { push } from 'react-router-redux';
import { Modal, Button } from 'react-bootstrap';

import Store from '../../store';
import IFilm from '../../models/IFilm';
import ITorrent from '../../models/ITorrent';
import TorrentList from '../torrents/TorrentList';

export type Props = {
    film: IFilm;
    torrent: ITorrent;
};

type ConnectedState = {};
type ConnectedDispatch = {
    goTo: (pathname: string) => void;
};

type CombinedProps = Props & ConnectedDispatch & ConnectedState;
class TorrentModalComponent extends React.Component<CombinedProps> {
    public render() {
        const film = this.props.film;
        const torrent = this.props.torrent;
        const onClose = () => {
            this.props.goTo(`/film/${film.id}`);
        };

        return (
            <Modal show={true} onHide={onClose}>
                <Modal.Header closeButton>
                    <Modal.Title>{film.title}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <ul className="list-group">
                        <InfoRow label="Release name" value={torrent.releaseName} />
                        <InfoRow label="Release group" value={torrent.releaseGroup} />
                        <InfoRow label="Codec" value={torrent.codec} />
                        <InfoRow label="Container" value={torrent.container} />
                        <InfoRow label="Cut" value={torrent.cut} />
                        <InfoRow label="Resolution" value={torrent.resolution} />
                        <InfoRow label="Source" value={torrent.sourceMedia} />
                        <InfoRow label="Uploaded at" value={torrent.uploadedAt} />
                        <InfoRow label="Uploaded by" value={torrent.uploadedBy} />
                    </ul>
                </Modal.Body>
                <Modal.Footer>
                    <Button bsStyle="primary" onClick={onClose}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }
}

interface IRowProps {
    label: string;
    value: string;
}
function InfoRow(props: IRowProps) {
    return (
        <li className="list-group-item">
            <strong>{props.label}</strong>: <span className="text-muted">{props.value}</span>
        </li>
    );
}

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    goTo: (pathname: string) => dispatch(push({ pathname: pathname }))
});

const TorrentModal: React.ComponentClass<Props> =
    connect(undefined, mapDispatchToProps)(TorrentModalComponent);
export default TorrentModal;
