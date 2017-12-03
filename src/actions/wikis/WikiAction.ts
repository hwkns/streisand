import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionHelper';

import { IUnkownError } from '../../models/base/IError';
import ErrorAction, { handleError } from '../ErrorAction';

import IWiki from '../../models/IWiki';

type WikiAction =
    { type: 'FETCHING_WIKI', id: number } |
    { type: 'RECEIVED_WIKI', wiki: IWiki } |
    { type: 'WIKI_FAILURE', id: number };
export default WikiAction;
type Action = WikiAction | ErrorAction;

function fetching(id: number): Action {
    return { type: 'FETCHING_WIKI', id };
}

function received(response: IWiki): Action {
    return {
        type: 'RECEIVED_WIKI',
        wiki: response
    };
}

function failure(id: number): Action {
    return { type: 'WIKI_FAILURE', id };
}

export function getWiki(id: number): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching(id));
        return fetch(state.auth.token, id).then((response: IWiki) => {
            return dispatch(received(response));
        }, (error: IUnkownError) => {
            dispatch(failure(id));
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string, id: number): Promise<IWiki> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/wikis/${id}/`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}