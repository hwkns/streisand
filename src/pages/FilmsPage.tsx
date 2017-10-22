import * as React from 'react';
import * as redux from 'redux';
import { connect } from 'react-redux';

import Store from '../store';
import { getFilms } from '../actions/FilmsAction';
import FilmsView from '../components/films/FilmsView';

export type Props = { };

type ConnectedState = {
    films: string[];
    isLoading: boolean;
};

type ConnectedDispatch = {
    getFilms: () => void;
};

type CombinedProps = ConnectedState & ConnectedDispatch & Props;
class FilmsPage extends React.Component<CombinedProps, void> {
    public componentWillMount() {
        if (!this.props.films.length && !this.props.isLoading) {
            this.props.getFilms();
        }
    }

    public render() {
        if (this.props.isLoading) {
            return ( <div>Loading...</div> );
        }

        const films = this.props.films;
        if (!films.length) {
            return (<div>No Forums found :(</div>);
        }

        return (
            <FilmsView films={films} />
        );
    }
}

const mapStateToProps = (state: Store.All, ownProps: Props): ConnectedState => ({
    isLoading: state.films.loading,
    films: state.films.allIds
});

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    getFilms: () => dispatch(getFilms())
});

export default connect(mapStateToProps, mapDispatchToProps)(FilmsPage);
