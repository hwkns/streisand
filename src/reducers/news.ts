import Store from '../store';
import Action from '../actions/NewsAction';
import INewsPost from '../models/INewsPost';
import { combineReducers } from './helpers';

function latest(state: INewsPost = null, action: Action): INewsPost {
    switch (action.type) {
        case 'RECEIVED_NEWS_POST':
            return action.post;
        default:
            return state;
    }
}

function loading(state: boolean = false, action: Action): boolean {
    switch (action.type) {
        case 'FETCHING_NEWS_POST':
            return true;
        case 'NEWS_POST_FAILURE':
        case 'RECEIVED_NEWS_POST':
            return false;
        default:
            return state;
    }
}

export default combineReducers<Store.News>({ latest, loading });