import * as objectAssign from 'object-assign';

import Store from '../store';
import Action from '../actions/WikiAction';
import IWiki from '../models/IWiki';
import { combineReducers } from './helpers';
import { IPage } from '../models/base/IPagedItemSet';

let counter = 1;
type ItemMap = { [id: number]: IWiki };
function byId(state: ItemMap = {}, action: Action): ItemMap {
    switch (action.type) {
        case 'RECEIVED_WIKIS':
            let map: ItemMap = {};
            for (const item of action.wikis) {
                if (!item.id) {
                    // TODO: remove this once the wiki api includes the id on the wiki response objects
                    item.id = counter++;
                }
                map[item.id] = item;
            }
            return objectAssign({}, state, map);
        default:
            return state;
    }
}

type Pages = { [page: number]: IPage<IWiki> };
function pages(state: Pages = {}, action: Action): Pages {
    let page: IPage<IWiki>;
    switch (action.type) {
        case 'FETCHING_WIKIS':
            page = objectAssign({ items: [] }, state[action.page], { loading: true });
            return objectAssign({}, state, { [action.page]: page });
        case 'RECEIVED_WIKIS':
            page = { loading: false, items: action.wikis };
            return objectAssign({}, state, { [action.page]: page });
        case 'WIKIS_FAILURE':
            page = objectAssign({ items: [] }, state[action.page], { loading: false });
            return objectAssign({}, state, { [action.page]: page });
        default:
            return state;
    }
}

function count(state: number = 0, action: Action): number {
    switch (action.type) {
        case 'RECEIVED_WIKIS':
            return action.count;
        default:
            return state;
    }
}

export default combineReducers<Store.Wikis>({ byId, count, pages });