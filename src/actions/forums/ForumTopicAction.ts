import Store from '../../store';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../ActionTypes';

import { transformTopic } from './transforms';
import { IUnkownError } from '../../models/base/IError';
import ErrorAction, { handleError } from '../ErrorAction';
import IPagedResponse from '../../models/base/IPagedResponse';
import { IForumGroupData } from '../../models/forums/IForumGroup';
import { IForumThreadResponse } from '../../models/forums/IForumThread';

type Response = IPagedResponse<IForumThreadResponse>;

type ForumTopicAction =
    { type: 'FETCHING_FORUM_TOPIC', id: number, page: number } |
    { type: 'RECEIVED_FORUM_TOPIC', id: number, page: number, count: number, data: IForumGroupData } |
    { type: 'FORUM_TOPIC_FAILURE', id: number, page: number };
export default ForumTopicAction;
type Action = ForumTopicAction | ErrorAction;

function fetching(id: number, page: number): Action {
    return { type: 'FETCHING_FORUM_TOPIC', id, page };
}

function received(id: number, page: number, response: Response): Action {
    return {
        type: 'RECEIVED_FORUM_TOPIC',
        id: id,
        page: page,
        count: response.count,
        data: transformTopic(response)
    };
}

function failure(id: number, page: number): Action {
    return { type: 'FORUM_TOPIC_FAILURE', id, page };
}

export function getThreads(id: number, page: number = 1): ThunkAction<Action> {
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
        url: `${globals.apiUrl}/forum-thread-index/?topic_id=${id}&page=${page}`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}