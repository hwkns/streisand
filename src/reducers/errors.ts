import { combineReducers } from 'redux';

import Store from '../store';
import AuthAction from '../actions/AuthAction';
import ErrorAction from '../actions/ErrorAction';

type Action = AuthAction | ErrorAction;

function authError(state: string = '', action: Action): string {
    switch (action.type) {
        case 'AUTHENTICATION_FAILED':
            return action.message;
        case 'AUTHENTICATED':
            return '';
        default:
            return state;
    }
}

function unkownError(state: string = '', action: Action): string {
    switch (action.type) {
        case 'UNKOWN_ERROR':
            return action.message;
        default:
            return state;
    }
}

export default combineReducers<Store.Errors>({ authError, unkownError });