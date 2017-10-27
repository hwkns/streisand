import * as React from 'react';
import { connect } from 'react-redux';

import FilmRow from './FilmRow';
import Store from '../../store';
import IFilm from '../../models/IFilm';

export type Props = {
    page: number;
};

type ConnectedState = {
    films: IFilm[];
};
type ConnectedDispatch = {};

type CombinedProps = Props & ConnectedDispatch & ConnectedState;
class FilmsViewComponent extends React.Component<CombinedProps> {
    public render() {
        const films = this.props.films;
        const rows = films.map((film: IFilm) => {
            return (<FilmRow film={film} key={film.id} />);
        });
        return (
            <div className="bs-component">
                <table className="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Name</th>
                            <th>Year</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        );
    }
}

const mapStateToProps = (state: Store.All, ownProps: Props): ConnectedState => {
    const page = state.films.pages[ownProps.page];
    return {
        films: page ? page.items : []
    };
};

const FilmsView: React.ComponentClass<Props> =
    connect(mapStateToProps)(FilmsViewComponent);
export default FilmsView;
