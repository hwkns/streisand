import * as assign from 'object-assign';

import IAuthInfo from '../models/IAuthInfo';
import Action from '../actions/AuthAction';

let authToken: string;
if (typeof sessionStorage !== 'undefined') {
    authToken = sessionStorage['jumpcut.token'] || undefined;
}

const defaultValue: IAuthInfo = {
    isAuthenticated: !!authToken,
    isAuthenticating: false,
    token: authToken
};

function storeToken(token: string) {
    if (typeof sessionStorage !== 'undefined') {
        sessionStorage['jumpcut.token'] = token;
    }
}

function auth(state: IAuthInfo = defaultValue, action: Action): IAuthInfo {
    switch (action.type) {
        case 'AUTHENTICATING':
            return assign({}, state, { isAuthenticating: true });
        case 'AUTHENTICATED':
            storeToken(action.token);
            return assign({}, state, {
                isAuthenticated: true,
                isAuthenticating: false,
                token: action.token
            });
        default:
            return state;
    }
}

export default auth;