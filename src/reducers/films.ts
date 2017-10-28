import { combineReducers } from 'redux';
import * as objectAssign from 'object-assign';

import Store from '../store';
import IFilm from '../models/IFilm';
import FilmAction from '../actions/FilmAction';
import FilmsAction from '../actions/FilmsAction';
import { IPage } from '../models/base/IPagedItemSet';

type Action = FilmsAction | FilmAction;

type ItemMap = { [id: string]: IFilm };
function byId(state: ItemMap = {}, action: Action): ItemMap {
    switch (action.type) {
        case 'FETCHING_FILM':
            return objectAssign({}, state, { [action.id]: { loading: true } });
        case 'RECEIVED_FILM':
            return objectAssign({}, state, { [action.film.id]: action.film });
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

type Pages = { [page: number]: IPage<IFilm> };
function pages(state: Pages = {}, action: Action): Pages {
    switch (action.type) {
        case 'FETCHING_FILMS':
            const page = objectAssign({ items: [] }, state[action.page], { loading: true });
            return objectAssign({}, state, { [action.page]: page });
        case 'RECEIVED_FILMS':
            const newPage = { loading: false, items: action.films };
            return objectAssign({}, state, { [action.page]: newPage });
        default:
            return state;
    }
}

function count(state: number = 0, action: Action): number {
    switch (action.type) {
        case 'RECEIVED_FILMS':
            return action.count;
        default:
            return state;
    }
}

export default combineReducers<Store.Films>({ byId, count, pages });