import * as React from 'react';
import * as redux from 'redux';
import { Link } from 'react-router';
import { connect } from 'react-redux';
import { replace } from 'react-router-redux';
import { Navbar, Nav, NavDropdown, MenuItem } from 'react-bootstrap';

import Store from '../store';
import { logout } from '../actions/AuthAction';
import { clearError } from '../actions/ErrorAction';
import Banner, { BannerType } from '../components/Banner';

export type Props = {};

type ConnectedState = {
    isAuthenticated: boolean;
    authError: string;
    errorMessage: string;
};

type ConnectedDispatch = {
    clearError: () => void;
    logout: () => void;
};

type CombinedProps = Props & ConnectedState & ConnectedDispatch;
class AppComponent extends React.Component<CombinedProps> {
    public render() {
        let logout;
        let links;

        if (this.props.isAuthenticated) {
            logout = this._getLogout();
            links = this._getLinks();
        }

        return (
            <div style={{'paddingTop': '80px'}}>
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
                <div className="container">
                    {this._getErrorBanner()}
                    {this.props.children}
                </div>
            </div>
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
            </Nav>
        );
    }

    private _getErrorBanner() {
        if (this.props.authError) {
            return <Banner type={BannerType.error}>{this.props.authError}</Banner>;
        }

        if (this.props.errorMessage) {
            const onClose = () => { this.props.clearError(); };
            return <Banner type={BannerType.error} onClose={onClose}>{this.props.errorMessage}</Banner>;
        }
    }
}

const mapStateToProps = (state: Store.All): ConnectedState => ({
    errorMessage: state.errors.unkownError,
    authError: state.errors.authError,
    isAuthenticated: state.auth.isAuthenticated
});

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    clearError: () => dispatch(clearError()),
    logout: () => {
        dispatch(logout());
        dispatch(replace('/login'));
    }
});

const App: React.ComponentClass<Props> =
    connect(mapStateToProps, mapDispatchToProps)(AppComponent);
export default App;