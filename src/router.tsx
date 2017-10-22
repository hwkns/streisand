import * as React from 'react';
import { Store as ReduxStore } from 'redux';
import { Route, Redirect, RouterState, RedirectFunction } from 'react-router';

import Store from './store';

import App from './pages/App';
import HomePage from './pages/HomePage';
import Themes from './components/Themes';
import FilmsPage from './pages/FilmsPage';
import LoginPage from './pages/LoginPage';
import AboutPage from './pages/AboutPage';

export function createRoutes(store: ReduxStore<Store.All>) {
    function checkAuth(nextState: RouterState, replace: RedirectFunction) {
        const state = store.getState();
        if (!state.auth.isAuthenticated) {
            replace('/login');
        }
    }

    return (
        <div>
            <Redirect from="/" to="/home" />
            <Route path="/" component={App}>
                <Route path="/login" component={LoginPage} />
                <Route path="/about" component={AboutPage} />
                <Route path="/themes" component={Themes} />
                <Route onEnter={checkAuth}>
                    <Route path="/home" component={HomePage} />
                    <Route path="/films" component={FilmsPage} />
                </Route>
                <Redirect from="*" to="/home" />
            </Route>
        </div>
    );
}
