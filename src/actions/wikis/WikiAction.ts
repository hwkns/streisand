import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionHelper';

import { IUnkownError } from '../../models/base/IError';
import ErrorAction, { handleError } from '../ErrorAction';

import IWiki, { IWikiUpdate } from '../../models/IWiki';

type WikiAction =
    { type: 'FETCHING_WIKI', id: number } |
    { type: 'RECEIVED_WIKI', wiki: IWiki } |
    { type: 'REMOVED_WIKI', id: number } |
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

function removed(id: number): Action {
    return { type: 'REMOVED_WIKI', id };
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

export function removeWiki(id: number): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        return remove(state.auth.token, id).then(() => {
            return dispatch(removed(id));
        }, (error: IUnkownError) => {
            dispatch(failure(id));
            return dispatch(handleError(error));
        });
    };
}

export function updateWiki(id: number, wiki: IWikiUpdate): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching(id));
        return update(state.auth.token, id, wiki).then((response: IWiki) => {
            return dispatch(received(response));
        }, (error: IUnkownError) => {
            dispatch(failure(id));
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string, id: number): Promise<IWiki> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/wiki-articles/${id}/`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}

function remove(token: string, id: number): Promise<void> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/wiki-articles/${id}/`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'DELETE'
    });
}

function update(token: string, id: number, wiki: IWikiUpdate): Promise<IWiki> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/wiki-articles/${id}/`,
        headers: {
            'Authorization': 'token ' + token,
            'Content-Type': 'application/json'
        },
        method: 'PUT',
        data: JSON.stringify(wiki)
    });
}