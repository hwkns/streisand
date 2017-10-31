import * as React from 'react';
import { connect } from 'react-redux';

import IFilm from '../../models/IFilm';

export type Props = {
    film: IFilm;
};

type ConnectedDispatch = {};
type ConnectedState = {};

type CombinedProps = Props & ConnectedDispatch & ConnectedState;
class FilmViewComponent extends React.Component<CombinedProps> {
    public render() {
        const film = this.props.film;
        const trailerId = getYouTubeId(film.trailerUrl);
        const youtubeUrl = `//www.youtube.com/embed/${trailerId}?rel=0&amp;wmode=transparent`;
        const tags = film.tags.map((tag: string) => {
            return (<span className="label label-default" key={tag}>{tag}</span>);
        });
        return (
            <div className="bs-component">
                <h1>{film.title}  [{film.year}]</h1>
                <div className="col-lg-8">
                    <div>
                        <iframe width="620" height="350" src={youtubeUrl} frameBorder="0"></iframe>
                    </div>
                    <div>
                        <h2>Description</h2>
                        <p>{film.description}</p>
                        <div>{tags}</div>
                    </div>
                </div>
                <div className="col-lg-3 col-lg-offset-1">
                    <img src={film.posterUrl} width="250px" />
                </div>
            </div>
        );
    }
}

const FilmView: React.ComponentClass<Props> =
    connect()(FilmViewComponent);
export default FilmView;

function getYouTubeId(url: string) {
    // TODO: server should return the youtube id so we don't have to parse it client side
    return url.substring(url.lastIndexOf('v=') + 2);
}