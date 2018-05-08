import ErrorAction from '../../ErrorAction';
import { fetchData } from '../../ActionHelper';
import { transformThread } from '../transforms';
import { ThunkAction } from '../../ActionTypes';
import globals from '../../../utilities/globals';
import { get } from '../../../utilities/Requestor';
import IPagedResponse from '../../../models/base/IPagedResponse';
import { IForumGroupData } from '../../../models/forums/IForumGroup';
import { IForumPostResponse } from '../../../models/forums/IForumPost';

type Response = IPagedResponse<IForumPostResponse>;

export type ForumThreadReceivedAction = {
    type: 'RECEIVED_FORUM_THREAD',
    id: number,
    page: number,
    count: number,
    data: IForumGroupData
};

type ForumThreadAction =
    { type: 'FETCHING_FORUM_THREAD', id: number, page: number } |
    ForumThreadReceivedAction |
    { type: 'FAILED_FORUM_THREAD', id: number, page: number } |
    { type: 'INVALIDATE_FORUM_THREAD', id: number, page: number };
export default ForumThreadAction;
type Action = ForumThreadAction | ErrorAction;

type Props = {
    id: number;
    page: number;
};

function fetching(props: Props): Action {
    return { type: 'FETCHING_FORUM_THREAD', id: props.id, page: props.page };
}

function received(props: Props, response: Response): Action {
    return {
        type: 'RECEIVED_FORUM_THREAD',
        id: props.id,
        page: props.page,
        count: response.count,
        data: transformThread(response)
    };
}

function failure(props: Props): Action {
    return { type: 'FAILED_FORUM_THREAD', id: props.id, page: props.page };
}

export function invalidate(props: Props) {
    return { type: 'INVALIDATE_FORUM_THREAD', id: props.id, page: props.page };
}

export function getPosts(id: number, page: number = 1): ThunkAction<Action> {
    const errorPrefix = `Fetching page ${page} of the forum thread (${id}) failed`;
    return fetchData({ request, fetching, received, failure, errorPrefix, props: { id, page } });
}

function request(token: string, props: Props): Promise<Response> {
    return get({ token, url: `${globals.apiUrl}/forum-posts/?thread_id=${props.id}&page=${props.page}` });
}