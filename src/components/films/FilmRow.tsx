import * as React from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';

import Store from '../../store';
import IFilm from '../../models/IFilm';

export type Props = {
    film: IFilm;
};

type CombinedProps = Props;
class FilmRowComponent extends React.Component<CombinedProps> {
    public render() {
        const film = this.props.film;
        return (
            <tr>
                <td>
                    <img src={film.posterUrl} width="80px" />
                </td>
                <td>
                    <Link to={'/film/' + film.id} title={film.title}>{film.title}</Link>
                </td>
                <td>
                    {film.year}
                </td>
            </tr>
        );
    }
}

const FilmRow: React.ComponentClass<Props> =
    connect()(FilmRowComponent);
export default FilmRow;