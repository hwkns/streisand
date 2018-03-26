import * as objectAssign from 'object-assign';

import Action from '../../actions/forums/ForumGroupsAction';
import { IPartialForumThread, IForumThread } from '../../models/forums/IForumThread';
import { combineReducers, mergeItem } from '../helpers';
import { IPage } from '../../models/base/IPagedItemSet';
import { ForumThreadData } from '../../models/forums/IForumData';

type ItemMap = { [id: number]: IPartialForumThread | IForumThread };
function byId(state: ItemMap = {}, action: Action): ItemMap {
    switch (action.type) {
        case 'RECEIVED_FORUM_GROUPS':
            let map: ItemMap = {};
            for (const item of action.data.threads) {
                mergeItem(map, item);
            }
            return objectAssign({}, state, map);
        default:
            return state;
    }
}

type Items = { [page: number]: IPage<IPartialForumThread | IForumThread> };
function pages(state: Items = {}, action: Action): Items {
    return state;
}

function count(state: number = 0, action: Action): number {
    return state;
}

export default combineReducers<ForumThreadData>({ byId, count, pages });