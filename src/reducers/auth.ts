import * as assign from 'object-assign';

import IAuthInfo from '../models/IAuthInfo';
import Action from '../actions/AuthAction';

const defaultValue: IAuthInfo = {
    isAuthenticated: false,
    isAuthenticating: false
};

function auth(state: IAuthInfo = defaultValue, action: Action): IAuthInfo {
    switch (action.type) {
        case 'AUTHENTICATING':
            return assign({}, state, { isAuthenticating: true });
        case 'AUTHENTICATED':
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