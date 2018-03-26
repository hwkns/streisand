import * as React from 'react';
import * as redux from 'redux';
import { Link } from 'react-router';
import { connect } from 'react-redux';
import { replace } from 'react-router-redux';
import { Navbar, Nav, NavDropdown, MenuItem } from 'react-bootstrap';

import Store from '../store';
import { logout } from '../actions/AuthAction';

export type Props = {};

type ConnectedState = {
    isAuthenticated: boolean;
};

type ConnectedDispatch = {
    logout: () => void;
};

type CombinedProps = Props & ConnectedState & ConnectedDispatch;
class SiteNavComponent extends React.Component<CombinedProps> {
    public render() {
        let logout;
        let links;

        if (this.props.isAuthenticated) {
            logout = this._getLogout();
            links = this._getLinks();
        }

        return (
            <Navbar fixedTop={true}>
                <Navbar.Header>
                    <Navbar.Brand>
                        <Link to="/">JumpCut</Link>
                    </Navbar.Brand>
                    <Navbar.Toggle />
                </Navbar.Header>
                <Navbar.Collapse>
                    {links}
                    <Nav pullRight>
                        <li role="presentation"><Link role="button" to="/about">About</Link></li>
                        <NavDropdown title="Settings" id="basic-nav-dropdown">
                            <li role="presentation"><Link role="menuitem" to="/themes">Themes</Link></li>
                            {logout}
                        </NavDropdown>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        );
    }

    private _getLogout() {
        const onLogout = () => {
            this.props.logout();
        };
        return (<MenuItem onClick={onLogout}>Logout</MenuItem>);
    }

    private _getLinks() {
        return (
            <Nav>
                <li role="presentation"><Link role="button" to="/films">Films</Link></li>
                <li role="presentation"><Link role="button" to="/torrents">Torrents</Link></li>
                <li role="presentation"><Link role="button" to="/wikis">Wikis</Link></li>
                <li role="presentation"><Link role="button" to="/forum">Forum</Link></li>
            </Nav>
        );
    }
}

const mapStateToProps = (state: Store.All): ConnectedState => ({
    isAuthenticated: state.auth.isAuthenticated
});

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    logout: () => {
        dispatch(logout());
        dispatch(replace('/login'));
    }
});

const SiteNav: React.ComponentClass<Props> =
    connect(mapStateToProps, mapDispatchToProps)(SiteNavComponent);
export default SiteNav;