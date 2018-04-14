import { ThunkAction } from '../ActionTypes';
import globals from '../../utilities/globals';
import Requestor from '../../utilities/Requestor';

import IWiki from '../../models/IWiki';
import ErrorAction from '../ErrorAction';
import { fetchData } from '../ActionHelper';

type WikiAction =
    { type: 'FETCHING_WIKI', id: number } |
    { type: 'RECEIVED_WIKI', wiki: IWiki } |
    { type: 'WIKI_FAILURE', id: number };
export default WikiAction;
type Action = WikiAction | ErrorAction;

function fetching(id: number): Action {
    return { type: 'FETCHING_WIKI', id };
}

function received(id: number, response: IWiki): Action {
    return {
        type: 'RECEIVED_WIKI',
        wiki: response
    };
}

function failure(id: number): Action {
    return { type: 'WIKI_FAILURE', id };
}

export function getWiki(id: number): ThunkAction<Action> {
    const errorPrefix = `Fetching wiki (${id}) failed`;
    return fetchData({ fetch, fetching, received, failure, errorPrefix, props: id });
}

function fetch(token: string, id: number): Promise<IWiki> {
    return Requestor.makeRequest({
        url: `${globals.apiUrl}/wikis/${id}/`,
        headers: {
            'Authorization': 'token ' + token
        },
        method: 'GET'
    });
}