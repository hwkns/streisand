import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionHelper';

import { IUnkownError } from '../../models/base/IError';
import ErrorAction, { handleError } from '../ErrorAction';

import IUser from '../../models/IUser';

type UserAction =
    { type: 'FETCHING_CURRENT_USER' } |
    { type: 'RECEIVED_CURRENT_USER', user: IUser } |
    { type: 'CURRENT_USER_FAILURE' };
export default UserAction;
type Action = UserAction | ErrorAction;

function fetching(): Action {
    return { type: 'FETCHING_CURRENT_USER' };
}

function received(response: IUser): Action {
    return {
        type: 'RECEIVED_CURRENT_USER',
        user: response
    };
}

function failure(): Action {
    return { type: 'CURRENT_USER_FAILURE' };
}

export function getCurrentUser(): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching());
        return fetch(state.auth.token).then((response: IUser) => {
            return dispatch(received(response));
        }, (error: IUnkownError) => {
            dispatch(failure());
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string): Promise<IUser> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/current-user/`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}