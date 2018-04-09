import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction } from '../ActionTypes';

import ErrorAction from '../ErrorAction';
import { transformGroups } from './transforms';
import { simplefetchData } from '../ActionHelper';
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
    const errorPrefix = 'Fetching the list of forums failed';
    return simplefetchData({ fetch, fetching, received, failure, errorPrefix });
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