import * as React from 'react';
import * as redux from 'redux';
import { connect } from 'react-redux';

import Store from '../../store';
import { IFilmUpdate } from '../../models/IFilm';
import CommandBar, { ICommand } from '../CommandBar';
import { TextInput, NumericInput } from '../generic/inputs';
import { createFilm } from '../../actions/films/CreateFilmAction';

export type Props = {};

type ConnectedState = {
    creating: boolean;
};

type ConnectedDispatch = {
    createFilm: (film: IFilmUpdate) => void;
};

type State = {
    title: string;
    description: string;
    duration?: number;
    imdbId: string;
    posterUrl: string;
    tmdbId?: number;
    trailerUrl: string;
    year: number;
};

type CombinedProps = Props & ConnectedDispatch & ConnectedState;
class CreateFilmViewComponent extends React.Component<CombinedProps, State> {
    constructor(props: CombinedProps) {
        super(props);

        this.state = {
            title: '',
            description: '',
            duration: undefined,
            imdbId: '',
            posterUrl: '',
            tmdbId: undefined,
            trailerUrl: '',
            year: (new Date()).getFullYear()
        };
    }

    public render() {
        const onCreateFilm = this._createFilm.bind(this);
        const create: ICommand = this.props.creating
            ? { label: 'creating film...' }
            : { label: 'Create film', onExecute: () => onCreateFilm() };
        return (
            <div>
                <CommandBar commands={[create]} />
                <form className="form-horizontal" onKeyPress={onCreateFilm} autoComplete="off">
                    <fieldset>
                        <TextInput id="imdb" label="IMDB identifier" placeholder="Corresponding imdb identifier"
                            value={this.state.imdbId} setValue={(value: string) => this.setState({ imdbId: value })} />
                        <NumericInput id="tmdb" label="TMDB identifier"
                            value={this.state.tmdbId} setValue={(value: number) => this.setState({ tmdbId: value })} />
                        <TextInput id="title" label="Title" placeholder="Film title"
                            value={this.state.title} setValue={(value: string) => this.setState({ title: value })} />
                        <TextInput id="description" label="Description" placeholder="Film description"
                            value={this.state.description} setValue={(value: string) => this.setState({ description: value })} />
                        <TextInput id="poster" label="Poster url" placeholder="Film poster"
                            value={this.state.posterUrl} setValue={(value: string) => this.setState({ posterUrl: value })} />
                        <TextInput id="trailer" label="Trailer url" placeholder="Youtube url or identifier"
                            value={this.state.trailerUrl} setValue={(value: string) => this.setState({ trailerUrl: value })} />
                        <NumericInput id="duration" label="Duration (in minutes)"
                            value={this.state.duration} setValue={(value: number) => this.setState({ duration: value })} />
                        <NumericInput id="year" label="Year of release"
                            value={this.state.year} setValue={(value: number) => this.setState({ year: value })} />
                    </fieldset>
                </form>
            </div>
        );
    }

    private _createFilm(event?: React.KeyboardEvent<HTMLElement>) {
        if (event && event.key !== 'Enter') {
            return;
        }

        const { title, description, duration, imdbId, posterUrl, tmdbId, trailerUrl, year } = this.state;
        if (title && description && duration && duration > 0 && imdbId && posterUrl && tmdbId && tmdbId > 0 && trailerUrl && year > 1800) {
            this.props.createFilm({
                title, description, imdbId, posterUrl, tmdbId, trailerUrl, year,
                durationInMinutes: duration,
                fanartUrl: '',
                moderationNotes: '',
                lists: [],
                trailerType: 'YouTube'
            });
        }
    }
}

const mapStateToProps = (state: Store.All, ownProps: Props): ConnectedState => ({
    creating: state.sealed.wikis.creating
});

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    createFilm: (film: IFilmUpdate) => dispatch(createFilm(film))
});

const CreateFilmView: React.ComponentClass<Props> =
    connect(mapStateToProps, mapDispatchToProps)(CreateFilmViewComponent);
export default CreateFilmView;