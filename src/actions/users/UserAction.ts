import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionHelper';

import { IUnkownError } from '../../models/base/IError';
import ErrorAction, { handleError } from '../ErrorAction';

import IUser, { IUserResponse } from '../../models/IUser';
import { transformUser } from './transforms';

type WikiAction =
    { type: 'FETCHING_USER', id: number } |
    { type: 'RECEIVED_USER', user: IUser } |
    { type: 'USER_FAILURE', id: number };
export default WikiAction;
type Action = WikiAction | ErrorAction;

function fetching(id: number): Action {
    return { type: 'FETCHING_USER', id };
}

function received(response: IUserResponse): Action {
    return {
        type: 'RECEIVED_USER',
        user: transformUser(response)
    };
}

function failure(id?: number): Action {
    return { type: 'USER_FAILURE', id };
}

export function getUser(id: number): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching(id));
        return fetch(state.sealed.auth.token, id).then((response: IUserResponse) => {
            return dispatch(received(response));
        }, (error: IUnkownError) => {
            dispatch(failure(id));
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string, id: number): Promise<IUserResponse> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/users/${id}/`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}