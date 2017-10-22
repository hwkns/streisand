import Store from '../store';
import globals from '../utilities/globals';
import Requestor from '../utilities/Requestor';
import { ThunkAction, IDispatch } from './ActionHelper';

import IFilm from '../models/IFilm';
import IPagedResponse from '../models/IPagedResponse';

type Action =
    { type: 'FETCHING_FILMS' } |
    { type: 'RECEIVED_FILMS', films: IFilm[] };
export default Action;

function fetching(): Action {
    return { type: 'FETCHING_FILMS' };
}

function received(response: IPagedResponse<IFilm>): Action {
    return {
        type: 'RECEIVED_FILMS',
        films: response.results
    };
}

export function getFilms(): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching());
        return fetch(state.auth.token).then((response: IPagedResponse<IFilm>) => {
            return dispatch(received(response));
        });
    };
}

function fetch(token: string): Promise<IPagedResponse<IFilm>> {
    // TODO: Add error handling
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/films`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}