import { replace } from 'react-router-redux';

import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';

import { logout } from './LogoutAction';
import { IUnkownError } from '../../models/base/IError';
import { ThunkAction, IDispatch } from '../ActionTypes';
import ErrorAction, { handleError } from '../ErrorAction';

type ChangePasswordAction =
    { type: 'UPDATING_PASSWORD' } |
    { type: 'UPDATED_PASSWORD' } |
    { type: 'FAILED_PASSWORD_UPDATE' };
export default ChangePasswordAction;
type Action = ChangePasswordAction | ErrorAction;

function updating(): Action {
    return { type: 'UPDATING_PASSWORD' };
}

function updated(): Action {
    return { type: 'UPDATED_PASSWORD' };
}

function failure(): Action {
    return { type: 'FAILED_PASSWORD_UPDATE' };
}

export function changePassword(oldPassword: string, newPassword: string): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(updating());
        return update(state.sealed.auth.token, oldPassword, newPassword).then((result: { token: string }) => {
            const action = dispatch(updated());
            dispatch(logout());
            dispatch(replace('/login'));
            return action;
        }, (error: IUnkownError) => {
            dispatch(failure());
            return dispatch(handleError(error));
        });
    };
}

function update(token: string, oldPassword: string, newPassword: string): Promise<{ token: string }> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/change-password/`,
        method: 'PUT',
        headers: {
            'Authorization': 'token ' + token,
            'Content-Type': 'application/json'
        },
        data: JSON.stringify({ oldPassword, newPassword })
    });
}
