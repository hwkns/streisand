import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionHelper';

import IWiki from '../../models/IWiki';
import { IUnkownError } from '../../models/base/IError';
import ErrorAction, { handleError } from '../ErrorAction';
import IPagedResponse from '../../models/base/IPagedResponse';

type WikiAction =
    { type: 'FETCHING_WIKIS', page: number } |
    { type: 'RECEIVED_WIKIS', page: number, count: number, wikis: IWiki[] } |
    { type: 'WIKIS_FAILURE', page: number };
export default WikiAction;
type Action = WikiAction | ErrorAction;

function fetching(page: number): Action {
    return { type: 'FETCHING_WIKIS', page };
}

function received(page: number, response: IPagedResponse<IWiki>): Action {
    return {
        page: page,
        count: response.count,
        type: 'RECEIVED_WIKIS',
        wikis: response.results
    };
}

function failure(page: number): Action {
    return { type: 'WIKIS_FAILURE', page };
}

export function getWikis(page: number = 1): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching(page));
        return fetch(state.sealed.auth.token, page).then((response: IPagedResponse<IWiki>) => {
            return dispatch(received(page, response));
        }, (error: IUnkownError) => {
            dispatch(failure(page));
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string, page: number): Promise<IPagedResponse<IWiki>> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/wiki-articles/?page=${page}`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}