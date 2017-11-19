import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionHelper';

import ITorrent from '../../models/ITorrent';
import { IUnkownError } from '../../models/base/IError';
import ErrorAction, { handleError } from '../ErrorAction';
import IPagedResponse from '../../models/base/IPagedResponse';

type FilmTorrentsAction =
    { type: 'FETCHING_FILM_TORRENTS', filmId: number, page: number } |
    { type: 'RECEIVED_FILM_TORRENTS', filmId: number, page: number, count: number, torrents: ITorrent[] } |
    { type: 'TORRENTS_FILM_FAILURE', filmId: number, page: number };
export default FilmTorrentsAction;
type Action = FilmTorrentsAction | ErrorAction;

function fetching(filmId: number, page: number): Action {
    return { type: 'FETCHING_FILM_TORRENTS', filmId, page };
}

function received(filmId: number, page: number, response: IPagedResponse<ITorrent>): Action {
    return {
        page: page,
        filmId: filmId,
        count: response.count,
        type: 'RECEIVED_FILM_TORRENTS',
        torrents: response.results
    };
}

function failure(filmId: number, page: number): Action {
    return { type: 'TORRENTS_FILM_FAILURE', filmId, page };
}

export function getTorrents(filmId: number, page: number = 1): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching(filmId, page));
        return fetch(state.auth.token, filmId, page).then((response: IPagedResponse<ITorrent>) => {
            return dispatch(received(filmId, page, response));
        }, (error: IUnkownError) => {
            dispatch(failure(filmId, page));
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string, filmId: number, page: number): Promise<IPagedResponse<ITorrent>> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/torrents?film_id=${filmId}&page=${page}`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}