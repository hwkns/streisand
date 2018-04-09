import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionTypes';

import { transformThread } from './transforms';
import { IUnkownError } from '../../models/base/IError';
import ErrorAction, { handleError } from '../ErrorAction';
import IPagedResponse from '../../models/base/IPagedResponse';
import { IForumGroupData } from '../../models/forums/IForumGroup';
import { IForumPostResponse } from '../../models/forums/IForumPost';

type Response = IPagedResponse<IForumPostResponse>;

type ForumTopicAction =
    { type: 'FETCHING_FORUM_THREAD', id: number, page: number } |
    { type: 'RECEIVED_FORUM_THREAD', id: number, page: number, count: number, data: IForumGroupData } |
    { type: 'FORUM_THREAD_FAILURE', id: number, page: number };
export default ForumTopicAction;
type Action = ForumTopicAction | ErrorAction;

function fetching(id: number, page: number): Action {
    return { type: 'FETCHING_FORUM_THREAD', id, page };
}

function received(id: number, page: number, response: Response): Action {
    return {
        type: 'RECEIVED_FORUM_THREAD',
        id: id,
        page: page,
        count: response.count,
        data: transformThread(response)
    };
}

function failure(id: number, page: number): Action {
    return { type: 'FORUM_THREAD_FAILURE', id, page };
}

export function getPosts(id: number, page: number = 1): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching(id, page));
        return fetch(state.sealed.auth.token, id, page).then((response: Response) => {
            return dispatch(received(id, page, response));
        }, (error: IUnkownError) => {
            dispatch(failure(id, page));
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string, id: number, page: number): Promise<Response> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/forum-posts/?thread_id=${id}&page=${page}`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}