import Store from '../store';
import globals from '../utilities/globals';
import Requestor from '../utilities/Requestor';
import { ThunkAction, IDispatch } from './ActionHelper';

import IFilm from '../models/IFilm';

type Action =
    { type: 'FETCHING_FILM', id: string } |
    { type: 'RECEIVED_FILM', film: IFilm };
export default Action;

function fetching(id: string): Action {
    return { type: 'FETCHING_FILM', id };
}

function received(response: IFilm): Action {
    return {
        type: 'RECEIVED_FILM',
        film: response
    };
}

export function getFilm(id: string): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching(id));
        return fetch(state.auth.token, id).then((response: IFilm) => {
            return dispatch(received(response));
        });
    };
}

function fetch(token: string, id: string): Promise<IFilm> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/films/${id}`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}