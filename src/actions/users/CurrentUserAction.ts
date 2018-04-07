import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionHelper';

import { transformUser } from './transforms';
import { IUnkownError } from '../../models/base/IError';
import IUser, { IUserResponse } from '../../models/IUser';
import ErrorAction, { handleError } from '../ErrorAction';

type UserAction =
    { type: 'FETCHING_CURRENT_USER' } |
    { type: 'RECEIVED_CURRENT_USER', user: IUser } |
    { type: 'CURRENT_USER_FAILURE' };
export default UserAction;
type Action = UserAction | ErrorAction;

function fetching(): Action {
    return { type: 'FETCHING_CURRENT_USER' };
}

function received(response: IUserResponse): Action {
    return {
        type: 'RECEIVED_CURRENT_USER',
        user: transformUser(response)
    };
}

function failure(): Action {
    return { type: 'CURRENT_USER_FAILURE' };
}

export function getCurrentUser(): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching());
        return fetch(state.sealed.auth.token).then((response: IUserResponse) => {
            return dispatch(received(response));
        }, (error: IUnkownError) => {
            dispatch(failure());
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string): Promise<IUserResponse> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/current-user/`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}