import * as React from 'react';
import * as redux from 'redux';
import { connect } from 'react-redux';

import Store from '../store';
import IFilm from '../models/IFilm';
import Empty from '../components/Empty';
import { getFilm } from '../actions/FilmAction';
import FilmView from '../components/films/FilmView';
import ILoadingItem from '../models/base/ILoadingItem';

export type Props = {
    params: {
        filmId: string;
    };
};

type ConnectedState = {
    film: IFilm;
    loading: boolean;
};

type ConnectedDispatch = {
    getFilm: (id: string) => void;
};

type CombinedProps = ConnectedState & ConnectedDispatch & Props;
class FilmPageComponent extends React.Component<CombinedProps, void> {
    public componentWillMount() {
        if (!this.props.loading) {
            this.props.getFilm(this.props.params.filmId);
        }
    }

    public componentWillReceiveProps(props: CombinedProps) {
        if (!props.loading && props.params.filmId !== this.props.params.filmId) {
            this.props.getFilm(props.params.filmId);
        }
    }

    public render() {
        const film = this.props.film;
        if (this.props.loading || !film) {
            return <Empty loading={this.props.loading} />;
        }

        return (
            <FilmView film={film} />
        );
    }
}

const mapStateToProps = (state: Store.All, ownProps: Props): ConnectedState => {
    const item = state.films.byId[ownProps.params.filmId];
    const loading = (item && (item as ILoadingItem).loading) || false;
    const film = (item && typeof (item as IFilm).id !== 'undefined') ? item as IFilm : undefined;

    return {
        loading: loading,
        film: film
    };
};

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    getFilm: (id: string) => dispatch(getFilm(id))
});

const FilmPage: React.ComponentClass<Props> =
    connect(mapStateToProps, mapDispatchToProps)(FilmPageComponent);
export default FilmPage;
