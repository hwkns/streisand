import { combineReducers } from 'redux';
import { routerReducer as routing } from 'react-router-redux';

import Store from '../store';

import auth from './auth';
import films from './films';
import errors from './errors';
import location from './location';

export const reducers = combineReducers<Store.All>({
    routing,
    auth,
    errors,
    location,
    films
});
