import { replace } from 'react-router-redux';

import Store from '../store';
import { IUnkownError } from '../models/base/IError';
import { ThunkAction, IDispatch } from './ActionHelper';

type Action =
    { type: 'AUTHENTICATION_FAILED', message: string } |
    { type: 'UNKOWN_ERROR', message: string };
export default Action;

function authfailure(message: string): Action {
    return { type: 'AUTHENTICATION_FAILED', message };
}

export function authError(error: IUnkownError): Action {
    const message = `Failed to login: ${JSON.stringify(error.result)}`;
    return authfailure(message);
}

export function handleError(error: IUnkownError): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        if (error.status === 401) {
            dispatch(authfailure('Authentication expired'));
            return dispatch(replace('/login'));
        }
        const message = `Unkown error (${error.status}): ${JSON.stringify(error.result)}`;
        return dispatch({ type: 'UNKOWN_ERROR', message });
    };
}