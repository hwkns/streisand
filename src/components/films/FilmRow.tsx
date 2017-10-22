import * as React from 'react';
import { connect } from 'react-redux';

import Store from '../../store';
import IFilm from '../../models/IFilm';

export type Props = {
    filmId: string;
};

type ConnectedState = {
    film: IFilm;
};

type CombinedProps = Props & ConnectedState;
class FilmRowComponent extends React.Component<CombinedProps> {
    public render() {
        const film = this.props.film;
        return (
            <tr>
                <td>
                    <img src={film.poster_url} width="80px" />
                </td>
                <td>
                    {film.title} ({film.year})
                </td>
            </tr>
        );
    }
}

const mapStateToProps = (state: Store.All, props: Props): ConnectedState => ({
    film: state.films.byId[props.filmId]
});

const FilmRow: React.ComponentClass<Props> =
    connect(mapStateToProps)(FilmRowComponent);
export default FilmRow;