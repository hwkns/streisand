import * as objectAssign from 'object-assign';

import Store from '../store';
import IUser from '../models/IUser';
import ForumAction from '../actions/forums';
import { combineReducers } from './helpers';
import { IPage } from '../models/base/IPagedItemSet';

type Action = ForumAction;

type ItemMap = { [id: number]: IUser };
function byId(state: ItemMap = {}, action: Action): ItemMap {
    switch (action.type) {
        case 'RECEIVED_FORUM_GROUPS':
        case 'RECEIVED_FORUM_TOPIC':
        case 'RECEIVED_FORUM_THREAD':
            const map: ItemMap = {};
            for (const item of action.data.users) {
                map[item.id] = item;
            }
            return objectAssign({}, state, map);
        default:
            return state;
    }
}

type Pages = { [page: number]: IPage<IUser> };
function pages(state: Pages = {}, action: Action): Pages {
    return state;
}

function count(state: number = 0, action: Action): number {
    return state;
}

export default combineReducers<Store.Users>({ byId, count, pages });