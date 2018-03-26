import * as objectAssign from 'object-assign';

import Action from '../../actions/forums/ForumGroupsAction';
import { IPartialForumPost, IForumPost } from '../../models/forums/IForumPost';
import { combineReducers, mergeItem } from '../helpers';
import { IPage } from '../../models/base/IPagedItemSet';
import { ForumPostData } from '../../models/forums/IForumData';

type ItemMap = { [id: number]: IPartialForumPost | IForumPost };
function byId(state: ItemMap = {}, action: Action): ItemMap {
    switch (action.type) {
        case 'RECEIVED_FORUM_GROUPS':
            let map: ItemMap = {};
            for (const item of action.data.posts) {
                mergeItem(map, item);
            }
            return objectAssign({}, state, map);
        default:
            return state;
    }
}

type Items = { [page: number]: IPage<IPartialForumPost | IForumPost> };
function pages(state: Items = {}, action: Action): Items {
    return state;
}

function count(state: number = 0, action: Action): number {
    return state;
}

export default combineReducers<ForumPostData>({ byId, count, pages });