import * as React from 'react';
import * as redux from 'redux';
import { connect } from 'react-redux';

import Store from '../../store';
import IFilm from '../../models/IFilm';
import Empty from '../../components/Empty';
import FilmView from '../../components/films/FilmView';
import { numericIdentifier } from '../../utilities/shim';
import { getFilm } from '../../actions/films/FilmAction';
import ILoadingItem from '../../models/base/ILoadingItem';
import { getTorrents } from '../../actions/torrents/FilmTorrentsAction';

export type Props = {
    params: {
        filmId: string;
        torrentId: string;
    };
};

type ConnectedState = {
    filmId: number;
    torrentId: number;
    film: IFilm;
    loading: boolean;
};

type ConnectedDispatch = {
    getFilm: (id: number) => void;
    getTorrents: (filmId: number) => void;
};

type CombinedProps = ConnectedState & ConnectedDispatch & Props;
class FilmPageComponent extends React.Component<CombinedProps, void> {
    public componentWillMount() {
        if (!this.props.loading) {
            this.props.getFilm(this.props.filmId);
            this.props.getTorrents(this.props.filmId);
        }
    }

    public componentWillReceiveProps(props: CombinedProps) {
        if (!props.loading && props.params.filmId !== this.props.params.filmId) {
            this.props.getFilm(props.filmId);
            this.props.getTorrents(props.filmId);
        }
    }

    public render() {
        const film = this.props.film;
        if (this.props.loading || !film) {
            return <Empty loading={this.props.loading} />;
        }

        return (
            <FilmView film={film} torrentId={this.props.torrentId} />
        );
    }
}

const mapStateToProps = (state: Store.All, ownProps: Props): ConnectedState => {
    const item = state.films.byId[ownProps.params.filmId];
    const loading = (item && (item as ILoadingItem).loading) || false;
    const film = (item && typeof (item as IFilm).id !== 'undefined') ? item as IFilm : undefined;

    return {
        loading: loading,
        film: film,
        filmId: numericIdentifier(ownProps.params.filmId),
        torrentId: numericIdentifier(ownProps.params.torrentId)
    };
};

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    getFilm: (id: number) => dispatch(getFilm(id)),
    getTorrents: (filmId: number) => dispatch(getTorrents(filmId))
});

const FilmPage: React.ComponentClass<Props> =
    connect(mapStateToProps, mapDispatchToProps)(FilmPageComponent);
export default FilmPage;
