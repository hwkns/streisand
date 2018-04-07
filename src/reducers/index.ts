import { routerReducer as routing } from 'react-router-redux';

import Store from '../store';
import { combineReducers } from './helpers';

import news from './news';
import auth from './auth';
import films from './films';
import wikis from './wikis';
import errors from './errors';
import forums from './forums';
import location from './location';
import torrents from './torrents';
import users from './users/users';
import deviceInfo from './deviceInfo';
import currentUser from './users/currentUser';

export default combineReducers<Store.All>({
    routing,
    auth,
    errors,
    currentUser,
    location,
    users,
    films,
    torrents,
    deviceInfo,
    wikis,
    news,
    forums
});
