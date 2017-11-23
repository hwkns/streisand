import { replace } from 'react-router-redux';

import Store from '../store';
import globals from '../utilities/globals';
import Requestor from '../utilities/Requestor';
import { IUnkownError } from '../models/base/IError';
import ErrorAction, { authError } from './ErrorAction';
import { ThunkAction, IDispatch } from './ActionHelper';

type AuthAction =
    { type: 'AUTHENTICATING' } |
    { type: 'AUTHENTICATED', token: string } |
    { type: 'AUTHENTICATION_FAILED', message: string };
export default AuthAction;
type Action = AuthAction | ErrorAction;

function authenticating(): Action {
    return { type: 'AUTHENTICATING' };
}

function authenticated(token: string): Action {
    return {
        type: 'AUTHENTICATED',
        token: token
    };
}

export function login(username: string, password: string): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(authenticating());
        return authenticate(username, password).then((result: { token: string }) => {
            const action = dispatch(authenticated(result.token));
            if (state.location.referrer) {
                dispatch(replace(state.location.referrer));
            }
            return action;
        }, (error: IUnkownError) => {
            return dispatch(authError(error));
        });
    };
}

function authenticate(username: string, password: string): Promise<{ token: string }> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/auth/`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        data: JSON.stringify({ username, password })
    });
}
