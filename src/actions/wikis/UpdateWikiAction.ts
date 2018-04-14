import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionTypes';

import WikiAction from './WikiAction';
import IWiki, { IWikiUpdate } from '../../models/IWiki';
import { IUnkownError } from '../../models/base/IError';
import ErrorAction, { handleError } from '../ErrorAction';

type UpdateWikiAction = { type: 'UDATING_WIKI', id: number };
export default UpdateWikiAction;
type Action = UpdateWikiAction | WikiAction | ErrorAction;

function updating(id: number): Action {
    return { type: 'UDATING_WIKI', id };
}

function received(id: number, response: IWiki): Action {
    return {
        type: 'RECEIVED_WIKI',
        wiki: response
    };
}

function failure(id: number): Action {
    return { type: 'WIKI_FAILURE', id };
}

export function updateWiki(id: number, wiki: IWikiUpdate): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(updating(id));
        return update(state.sealed.auth.token, id, wiki).then((response: IWiki) => {
            return dispatch(received(id, response));
        }, (error: IUnkownError) => {
            dispatch(failure(id));
            return dispatch(handleError(error));
        });
    };
}

function update(token: string, id: number, wiki: IWikiUpdate): Promise<IWiki> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/wikis/${id}/`,
        headers: {
            'Authorization': 'token ' + token,
            'Content-Type': 'application/json'
        },
        method: 'PUT',
        data: JSON.stringify(wiki)
    });
}