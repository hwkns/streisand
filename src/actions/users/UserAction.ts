import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionHelper';

import { IUnkownError } from '../../models/base/IError';
import ErrorAction, { handleError } from '../ErrorAction';

import IUser from '../../models/IUser';

type WikiAction =
    { type: 'FETCHING_USER', id: number } |
    { type: 'RECEIVED_USER', user: IUser } |
    { type: 'USER_FAILURE', id: number };
export default WikiAction;
type Action = WikiAction | ErrorAction;

function fetching(id: number): Action {
    return { type: 'FETCHING_USER', id };
}

function received(response: IUser): Action {
    return {
        type: 'RECEIVED_USER',
        user: response
    };
}

function failure(id?: number): Action {
    return { type: 'USER_FAILURE', id };
}

export function getUser(id: number): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching(id));
        return fetch(state.auth.token, id).then((response: IUser) => {
            return dispatch(received(response));
        }, (error: IUnkownError) => {
            dispatch(failure(id));
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string, id: number): Promise<IUser> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/users/${id}/`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}