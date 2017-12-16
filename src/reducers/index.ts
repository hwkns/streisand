import { routerReducer as routing } from 'react-router-redux';

import Store from '../store';
import { combineReducers } from './helpers';

import news from './news';
import auth from './auth';
import films from './films';
import wikis from './wikis';
import errors from './errors';
import location from './location';
import torrents from './torrents';
import deviceInfo from './deviceInfo';

export const reducers = combineReducers<Store.All>({
    routing,
    auth,
    errors,
    location,
    films,
    torrents,
    deviceInfo,
    wikis,
    news
});
