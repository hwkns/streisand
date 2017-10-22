import * as React from 'react';
import { connect } from 'react-redux';

// import Store from '../../store';
import FilmRow from './FilmRow';

export type Props = {
    films: string[];
};

type ConnectedDispatch = {};
type ConnectedState = {};

type CombinedProps = Props & ConnectedDispatch & ConnectedState;
class FilmsViewComponent extends React.Component<CombinedProps> {
    public render() {
        const films = this.props.films;
        const rows = films.map((id: string) => {
            return (<FilmRow filmId={id} key={id} />);
        });
        return (
            <div className="bs-component">
                <table className="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Name</th>
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

const FilmsView: React.ComponentClass<Props> =
    connect()(FilmsViewComponent);
export default FilmsView;
