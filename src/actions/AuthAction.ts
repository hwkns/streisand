import { replace } from 'react-router-redux';

import Store from '../store';
import globals from '../utilities/globals';
import Requestor from '../utilities/Requestor';

type AuthAction =
    { type: 'AUTHENTICATING' } |
    { type: 'AUTHENTICATED', token: string };
export default AuthAction;

interface IDispatch { (action: AuthAction | ThunkAction): AuthAction; }
type ThunkAction = (dispatch: IDispatch, getState: () => Store.All) => AuthAction | ThunkAction | Promise<AuthAction | ThunkAction>;

function authenticating(): AuthAction {
    return { type: 'AUTHENTICATING' };
}

function authenticated(token: string): AuthAction {
    return {
        type: 'AUTHENTICATED',
        token: token
    };
}

export function login(username: string, password: string): ThunkAction {
    return (dispatch: IDispatch, getState: () => Store.All) => {
        const state = getState();
        dispatch(authenticating());
        return authenticate(username, password).then((result: { token: string }) => {
            const action = dispatch(authenticated(result.token));
            if (state.location.referrer) {
                dispatch(replace(state.location.referrer));
            }
            return action;
        });
    };
}

function authenticate(username: string, password: string): Promise<{ token: string }> {
    // TODO: Add error handling
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/auth`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        data: JSON.stringify({ username, password })
    });
}
