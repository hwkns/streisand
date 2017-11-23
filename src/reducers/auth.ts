import * as assign from 'object-assign';

import IAuthInfo from '../models/IAuthInfo';
import Action from '../actions/AuthAction';
import { getAuthToken } from '../utilities/storage';

const authToken = getAuthToken();
const defaultValue: IAuthInfo = {
    isAuthenticated: !!authToken,
    isAuthenticating: false,
    token: authToken
};

function auth(state: IAuthInfo = defaultValue, action: Action): IAuthInfo {
    switch (action.type) {
        case 'LOGOUT':
        case 'AUTHENTICATION_FAILED':
            return {
                isAuthenticated: false,
                isAuthenticating: false,
                token: undefined
            };
        case 'AUTHENTICATING':
            return assign({}, state, { isAuthenticating: true });
        case 'AUTHENTICATED':
            return {
                isAuthenticated: true,
                isAuthenticating: false,
                token: action.token
            };
        default:
            return state;
    }
}

export default auth;