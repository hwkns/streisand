import Store from '../store';
import globals from '../utilities/globals';
import Requestor from '../utilities/Requestor';
import { ThunkAction, IDispatch } from './ActionHelper';

import IFilm from '../models/IFilm';
import ILoadingItem from '../models/base/ILoadingItem';
import IPagedResponse from '../models/base/IPagedResponse';

type Action =
    { type: 'FETCHING_FILMS', page: number } |
    { type: 'RECEIVED_FILMS', page: number, count: number, films: IFilm[] };
export default Action;

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

export function getFilms(page: number = 1): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching(page));
        return fetch(state.auth.token, page).then((response: IPagedResponse<IFilm>) => {
            return dispatch(received(page, response));
        });
    };
}

function fetch(token: string, page: number): Promise<IPagedResponse<IFilm>> {
    // TODO: Add error handling
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/films?page=${page}`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}