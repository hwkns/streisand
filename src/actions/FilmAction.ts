import Store from '../store';
import globals from '../utilities/globals';
import Requestor from '../utilities/Requestor';
import { ThunkAction, IDispatch } from './ActionHelper';

import IFilm from '../models/IFilm';

type Action =
    { type: 'FETCHING_FILMS' } |
    { type: 'RECEIVED_FILMS', films: IFilm[] };
export default Action;

function fetching(): Action {
    return { type: 'FETCHING_FILMS' };
}

function received(response: IFilm): Action {
    return {
        type: 'RECEIVED_FILMS',
        films: [response]
    };
}

export function getFilm(id: string): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching());
        return fetch(id, state.auth.token).then((response: IFilm) => {
            return dispatch(received(response));
        });
    };
}

function fetch(id: string, token: string): Promise<IFilm> {
    // TODO: Add error handling
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/films/${id}`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}