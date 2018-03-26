import * as React from 'react';
import { Store as ReduxStore } from 'redux';
import { Route, Redirect, RouterState, RedirectFunction } from 'react-router';

import Store from './store';

import App from './pages/App';
import Themes from './components/Themes';
import AboutPage from './pages/AboutPage';
import LoginPage from './pages/LoginPage';

import HomePage from './pages/HomePage';

import WikiPage from './pages/wikis/WikiPage';
import WikisPage from './pages/wikis/WikisPage';

import FilmPage from './pages/films/FilmPage';
import FilmsPage from './pages/films/FilmsPage';
import TorrentsPage from './pages/TorrentsPage';

import ForumPage from './pages/forums/ForumPage';

export function createRoutes(store: ReduxStore<Store.All>) {
    function requireAuth(nextState: RouterState, replace: RedirectFunction) {
        if (!store.getState().auth.isAuthenticated) {
            replace('/login');
        }
    }

    function checkAuth(nextState: RouterState, replace: RedirectFunction) {
        if (store.getState().auth.isAuthenticated) {
            replace('/');
        }
    }

    return (
        <div>
            <Redirect from="/" to="/home" />
            <Route path="/" component={App}>
                <Route path="/login" component={LoginPage} onEnter={checkAuth} />
                <Route path="/about" component={AboutPage} />
                <Route path="/themes" component={Themes} />
                <Route onEnter={requireAuth}>
                    <Route path="/home" component={HomePage} />

                    <Route path="/films/:page" component={FilmsPage} />
                    <Redirect from="/films" to="/films/1" />
                    <Route path="/film/:filmId" component={FilmPage} />
                    <Route path="/film/:filmId/:torrentId" component={FilmPage} />
                    <Redirect from="/film" to="/films/1" />

                    <Route path="/torrents/:page" component={TorrentsPage} />
                    <Redirect from="/torrents" to="/torrents/1" />

                    <Route path="/wikis/:page" component={WikisPage} />
                    <Redirect from="/wikis" to="/wikis/1" />
                    <Route path="/wiki/:wikiId" component={WikiPage} />
                    <Redirect from="/wiki" to="/wikis/1" />

                    <Route path="/forum" component={ForumPage} />
                </Route>
                <Redirect from="*" to="/home" />
            </Route>
        </div>
    );
}
