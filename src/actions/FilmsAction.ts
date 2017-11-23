import Store from '../store';
import globals from '../utilities/globals';
import Requestor from '../utilities/Requestor';
import { ThunkAction, IDispatch } from './ActionHelper';

import IFilm from '../models/IFilm';
import { IUnkownError } from '../models/base/IError';
import IPagedResponse from '../models/base/IPagedResponse';
import ErrorAction, { handleError } from './ErrorAction';

type FilmsAction =
    { type: 'FETCHING_FILMS', page: number } |
    { type: 'RECEIVED_FILMS', page: number, count: number, films: IFilm[] } |
    { type: 'FILMS_FAILURE', page: number };
export default FilmsAction;
type Action = FilmsAction | ErrorAction;

function fetching(page: number): Action {
    return { type: 'FETCHING_FILMS', page };
}

function received(page: number, response: IPagedResponse<IFilm>): Action {
    return {
        page: page,
        count: response.count,
        type: 'RECEIVED_FILMS',
        films: response.results
    };
}

function failure(page: number): Action {
    return { type: 'FILMS_FAILURE', page };
}

export function getFilms(page: number = 1): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching(page));
        return fetch(state.auth.token, page).then((response: IPagedResponse<IFilm>) => {
            return dispatch(received(page, response));
        }, (error: IUnkownError) => {
            dispatch(failure(page));
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string, page: number): Promise<IPagedResponse<IFilm>> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/films/?page=${page}`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}