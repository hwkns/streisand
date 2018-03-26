
import { combineReducers } from '../helpers';
import IForumGroup from '../../models/forums/IForumGroup';
import Action from '../../actions/forums/ForumGroupsAction';
import { ForumGroupData } from '../../models/forums/IForumData';

function items(state: IForumGroup[] = [], action: Action): IForumGroup[] {
    switch (action.type) {
        case 'RECEIVED_FORUM_GROUPS':
            return action.data.groups;
        default:
            return state;
    }
}

function loading(state: boolean = false, action: Action): boolean {
    switch (action.type) {
        case 'FETCHING_FORUM_GROUPS':
            return true;
        case 'FORUM_GROUPS_FAILURE':
        case 'RECEIVED_FORUM_GROUPS':
            return false;
        default:
            return state;
    }
}

export default combineReducers<ForumGroupData>({ loading, items });