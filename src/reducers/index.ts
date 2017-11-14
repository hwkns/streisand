import { routerReducer as routing } from 'react-router-redux';

import Store from '../store';
import { combineReducers } from './helpers';

import auth from './auth';
import films from './films';
import errors from './errors';
import location from './location';
import torrents from './torrents';

export const reducers = combineReducers<Store.All>({
    routing,
    auth,
    errors,
    location,
    films,
    torrents
});
