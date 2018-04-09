import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionTypes';

import { transformGroups } from './transforms';
import { IUnkownError } from '../../models/base/IError';
import ErrorAction, { handleError } from '../ErrorAction';
import IPagedResponse from '../../models/base/IPagedResponse';
import { IForumGroupResponse, IForumGroupData } from '../../models/forums/IForumGroup';

type ForumGroupsction =
    { type: 'FETCHING_FORUM_GROUPS' } |
    { type: 'RECEIVED_FORUM_GROUPS', data: IForumGroupData } |
    { type: 'FORUM_GROUPS_FAILURE' };
export default ForumGroupsction;
type Action = ForumGroupsction | ErrorAction;

function fetching(): Action {
    return { type: 'FETCHING_FORUM_GROUPS' };
}

function received(response: IPagedResponse<IForumGroupResponse>): Action {
    return {
        type: 'RECEIVED_FORUM_GROUPS',
        data: transformGroups(response)
    };
}

function failure(): Action {
    return { type: 'FORUM_GROUPS_FAILURE' };
}

export function getForumGroups(): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching());
        return fetch(state.sealed.auth.token).then((response: IPagedResponse<IForumGroupResponse>) => {
            return dispatch(received(response));
        }, (error: IUnkownError) => {
            dispatch(failure());
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string): Promise<IPagedResponse<IForumGroupResponse>> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/forum-groups/`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}