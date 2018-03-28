import * as objectAssign from 'object-assign';

import { combineReducers } from '../helpers';
import { INestedPages } from '../../models/base/IPagedItemSet';
import { IForumPost } from '../../models/forums/IForumPost';
import { ForumPostData } from '../../models/forums/IForumData';
import ForumTopicAction from '../../actions/forums/ForumTopicAction';
import ForumGroupsAction from '../../actions/forums/ForumGroupsAction';

type Action = ForumGroupsAction | ForumTopicAction;

type ItemMap = { [id: number]: IForumPost };
function byId(state: ItemMap = {}, action: Action): ItemMap {
    switch (action.type) {
        case 'RECEIVED_FORUM_GROUPS':
        case 'RECEIVED_FORUM_TOPIC':
            let map: ItemMap = {};
            for (const item of action.data.posts) {
                map[item.id] = item;
            }
            return objectAssign({}, state, map);
        default:
            return state;
    }
}

type Items = INestedPages<IForumPost>;
function byThread(state: Items = {}, action: Action): Items {
    return state;
}

export default combineReducers<ForumPostData>({ byId, byThread });