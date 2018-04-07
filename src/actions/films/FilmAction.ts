import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionHelper';

import { IUnkownError } from '../../models/base/IError';
import ErrorAction, { handleError } from '../ErrorAction';

import IFilm from '../../models/IFilm';

type FilmAction =
    { type: 'FETCHING_FILM', id: number } |
    { type: 'RECEIVED_FILM', film: IFilm } |
    { type: 'FILM_FAILURE', id: number };
export default FilmAction;
type Action = FilmAction | ErrorAction;

function fetching(id: number): Action {
    return { type: 'FETCHING_FILM', id };
}

function received(response: IFilm): Action {
    return {
        type: 'RECEIVED_FILM',
        film: response
    };
}

function failure(id: number): Action {
    return { type: 'FILM_FAILURE', id };
}

export function getFilm(id: number): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching(id));
        return fetch(state.sealed.auth.token, id).then((response: IFilm) => {
            return dispatch(received(response));
        }, (error: IUnkownError) => {
            dispatch(failure(id));
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string, id: number): Promise<IFilm> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/films/${id}/`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}