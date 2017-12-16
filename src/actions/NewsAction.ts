import Store from '../store';
import globals from '../utilities/globals';
import Requestor from '../utilities/Requestor';
import { ThunkAction, IDispatch } from './ActionHelper';

import { IUnkownError } from '../models/base/IError';
import ErrorAction, { handleError } from './ErrorAction';

import INewsPost from '../models/INewsPost';

type NewsAction =
    { type: 'FETCHING_NEWS_POST' } |
    { type: 'RECEIVED_NEWS_POST', post: INewsPost } |
    { type: 'NEWS_POST_FAILURE' };
export default NewsAction;
type Action = NewsAction | ErrorAction;

function fetching(): Action {
    return { type: 'FETCHING_NEWS_POST' };
}

function received(post: INewsPost): Action {
    return { type: 'RECEIVED_NEWS_POST', post: post };
}

function failure(): Action {
    return { type: 'NEWS_POST_FAILURE' };
}

export function getLatestNews(): ThunkAction<Action> {
    return (dispatch: IDispatch<Action>, getState: () => Store.All) => {
        const state = getState();
        dispatch(fetching());
        return fetch(state.auth.token).then((response: INewsPost) => {
            return dispatch(received(response));
        }, (error: IUnkownError) => {
            dispatch(failure());
            return dispatch(handleError(error));
        });
    };
}

function fetch(token: string): Promise<INewsPost> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/news-posts/latest/`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}