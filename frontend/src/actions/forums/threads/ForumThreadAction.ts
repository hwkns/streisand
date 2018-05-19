import Store from '../../../store';
import ErrorAction from '../../ErrorAction';
import { fetchData } from '../../ActionHelper';
import { transformThread } from '../transforms';
import globals from '../../../utilities/globals';
import { get } from '../../../utilities/Requestor';
import { ThunkAction, IDispatch } from '../../ActionTypes';
import { IForumGroupData } from '../../../models/forums/IForumGroup';
import BulkUserAction, { getUsers } from '../../users/BulkUserAction';
import { IForumThreadResponse } from '../../../models/forums/IForumThread';

const PAGE_SIZE = globals.pageSize.posts;
export type ForumThreadReceivedAction = {
    type: 'RECEIVED_FORUM_THREAD',
    id: number,
    page: number,
    count: number,
    pageSize: number,
    data: IForumGroupData
};

type ForumThreadAction =
    { type: 'FETCHING_FORUM_THREAD', id: number, page: number } |
    ForumThreadReceivedAction |
    { type: 'FAILED_FORUM_THREAD', id: number, page: number } |
    { type: 'INVALIDATE_FORUM_THREAD', id: number, page: number };
export default ForumThreadAction;
type Action = ForumThreadAction | BulkUserAction | ErrorAction;

type Props = {
    id: number;
    page: number;
};

function fetching(props: Props): Action {
    return { type: 'FETCHING_FORUM_THREAD', id: props.id, page: props.page };
}

function received(props: Props, response: IForumThreadResponse): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const data = transformThread(response);
        if (data.users.length) {
            dispatch(getUsers(data.users));
        }
        return dispatch({
            type: 'RECEIVED_FORUM_THREAD',
            id: props.id,
            page: props.page,
            pageSize: PAGE_SIZE,
            count: response.posts.count,
            data: data
        });
    };
}

function failure(props: Props): Action {
    return { type: 'FAILED_FORUM_THREAD', id: props.id, page: props.page };
}

export function invalidate(props: Props): Action {
    return { type: 'INVALIDATE_FORUM_THREAD', id: props.id, page: props.page };
}

export function getPosts(id: number, page: number = 1): ThunkAction<Action> {
    const errorPrefix = `Fetching page ${page} of the forum thread (${id}) failed`;
    return fetchData({ request, fetching, received, failure, errorPrefix, props: { id, page } });
}

function request(token: string, props: Props): Promise<IForumThreadResponse> {
    return get({ token, url: `${globals.apiUrl}/forum-thread-index/${props.id}/?page=${props.page}&size=${PAGE_SIZE}` });
}