import { ThunkAction } from '../ActionTypes';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';

import ErrorAction from '../ErrorAction';
import { transformUser } from './transforms';
import { simplefetchData } from '../ActionHelper';
import IUser, { IUserResponse } from '../../models/IUser';

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
    const errorPrefix = 'Fetching current user information failed';
    return simplefetchData({ fetch, fetching, received, failure, errorPrefix });
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