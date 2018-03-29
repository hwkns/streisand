import { routerReducer as routing } from 'react-router-redux';

import Store from '../store';
import { combineReducers } from './helpers';

import news from './news';
import auth from './auth';
import users from './users';
import films from './films';
import wikis from './wikis';
import errors from './errors';
import forums from './forums';
import location from './location';
import torrents from './torrents';
import deviceInfo from './deviceInfo';

export default combineReducers<Store.All>({
    routing,
    auth,
    errors,
    location,
    users,
    films,
    torrents,
    deviceInfo,
    wikis,
    news,
    forums
});
