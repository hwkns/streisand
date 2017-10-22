import { combineReducers } from 'redux';
import * as objectAssign from 'object-assign';

import Store from '../store';
import IFilm from '../models/IFilm';
import Action from '../actions/FilmsAction';

function allIds(state: string[] = [], action: Action): string[] {
    switch (action.type) {
        case 'RECEIVED_FILMS':
            return [
                ...state,
                ...action.films.map((item: IFilm) => item.id)
            ];
        default:
            return state;
    }
}

type ItemMap = { [id: string]: IFilm };
function byId(state: ItemMap = {}, action: Action): ItemMap {
    switch (action.type) {
        case 'RECEIVED_FILMS':
            let map: ItemMap = {};
            for (const item of action.films) {
                map[item.id] = item;
            }
            return objectAssign({}, state, map);
        default:
            return state;
    }
}

function loading(state: boolean = false, action: Action): boolean {
    switch (action.type) {
        case 'FETCHING_FILMS':
            return true;
        case 'RECEIVED_FILMS':
            return false;
        default:
            return state;
    }
}

export default combineReducers<Store.Films>({
    loading: loading,
    byId: byId,
    allIds: allIds
});