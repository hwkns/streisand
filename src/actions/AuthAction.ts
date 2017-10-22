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
        dispatch(authenticating());
        return authenticate(username, password).then((result: { token: string }) => {
            return dispatch(authenticated(result.token));
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
