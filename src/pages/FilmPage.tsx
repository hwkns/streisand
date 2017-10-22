import * as React from 'react';
import * as redux from 'redux';
import { connect } from 'react-redux';

import Store from '../store';
import IFilm from '../models/IFilm';
import { getFilm } from '../actions/FilmAction';
import FilmView from '../components/films/FilmView';

export type Props = {
    params: {
        filmId: string;
    };
};

type ConnectedState = {
    film: IFilm;
    isLoading: boolean;
};

type ConnectedDispatch = {
    getFilm: (id: string) => void;
};

type CombinedProps = ConnectedState & ConnectedDispatch & Props;
class FilmPageComponent extends React.Component<CombinedProps, void> {
    public componentWillMount() {
        if (!this.props.film && !this.props.isLoading) {
            this.props.getFilm(this.props.params.filmId);
        }
    }

    public render() {
        if (this.props.isLoading) {
            return (<div>Loading...</div>);
        }

        const film = this.props.film;
        if (!film) {
            return (<div>Film not found :(</div>);
        }

        return (
            <FilmView film={film} />
        );
    }
}

const mapStateToProps = (state: Store.All, ownProps: Props): ConnectedState => ({
    isLoading: state.films.loading,
    film: state.films.byId[ownProps.params.filmId]
});

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    getFilm: (id: string) => dispatch(getFilm(id))
});

const FilmPage: React.ComponentClass<Props> =
    connect(mapStateToProps, mapDispatchToProps)(FilmPageComponent);
export default FilmPage;
