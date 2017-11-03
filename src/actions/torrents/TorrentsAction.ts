import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionHelper';

import ITorrent from '../../models/ITorrent';
import { IUnkownError } from '../../models/base/IError';
import ILoadingItem from '../../models/base/ILoadingItem';
import ErrorAction, { handleError } from '../ErrorAction';
import IPagedResponse from '../../models/base/IPagedResponse';

type TorrentsAction =
    { type: 'FETCHING_TORRENTS', page: number } |
    { type: 'RECEIVED_TORRENTS', page: number, count: number, torrents: ITorrent[] } |
    { type: 'TORRENTS_FAILURE', page: number };
export default TorrentsAction;
type Action = TorrentsAction | ErrorAction;

function fetching(page: number): Action {
    return { type: 'FETCHING_TORRENTS', page };
}

function received(page: number, response: IPagedResponse<ITorrent>): Action {
    return {
        page: page,
        count: response.count,
        type: 'RECEIVED_TORRENTS',
        torrents: response.results
    };
}

function failure(page: number): Action {
    return { type: 'TORRENTS_FAILURE', page };
}

export function getTorrents(page: number = 1): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching(page));
        return fetch(state.auth.token, page).then((response: IPagedResponse<ITorrent>) => {
            return dispatch(received(page, response));
        }, (error: IUnkownError) => {
            dispatch(failure(page));
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string, page: number): Promise<IPagedResponse<ITorrent>> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/torrents?page=${page}`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}