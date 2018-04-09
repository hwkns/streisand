import { ThunkAction } from '../ActionTypes';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';

import ErrorAction from '../ErrorAction';
import { fetchData } from '../ActionHelper';
import { transformUser } from './transforms';
import IUser, { IUserResponse } from '../../models/IUser';

type WikiAction =
    { type: 'FETCHING_USER', id: number } |
    { type: 'RECEIVED_USER', user: IUser } |
    { type: 'USER_FAILURE', id: number };
export default WikiAction;
type Action = WikiAction | ErrorAction;

function fetching(id: number): Action {
    return { type: 'FETCHING_USER', id };
}

function received(id: number, response: IUserResponse): Action {
    return {
        type: 'RECEIVED_USER',
        user: transformUser(response)
    };
}

function failure(id: number): Action {
    return { type: 'USER_FAILURE', id };
}

export function getUser(id: number): ThunkAction<Action> {
    const errorPrefix = `Fetching film (${id}) failed`;
    return fetchData({ fetch, fetching, received, failure, errorPrefix, props: id });
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