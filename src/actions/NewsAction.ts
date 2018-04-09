import globals from '../utilities/globals';
import { ThunkAction } from './ActionTypes';
import Requestor from '../utilities/Requestor';

import ErrorAction from './ErrorAction';
import { fetchData } from './ActionHelper';
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
    const errorPrefix = 'Fetching latest news failed';
    return fetchData({ fetch, fetching, received, failure, errorPrefix });
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