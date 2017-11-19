import * as React from 'react';
import * as redux from 'redux';
import { Link } from 'react-router';
import { connect } from 'react-redux';
import { Navbar, Nav, MenuItem, NavItem, NavDropdown } from 'react-bootstrap';

import Store from '../store';
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
};

type CombinedProps = Props & ConnectedState & ConnectedDispatch;
class AppComponent extends React.Component<CombinedProps> {
    public render() {
        const links = !this.props.isAuthenticated ? undefined : (
            <Nav>
                <li role="presentation"><Link role="button" to="/films">Films</Link></li>
                <li role="presentation"><Link role="button" to="/torrents">Torrents</Link></li>
            </Nav>
        );
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

const mapStateToProps = (state: Store.All, props: Props): ConnectedState => ({
    errorMessage: state.errors.unkownError,
    authError: state.errors.authError,
    isAuthenticated: state.auth.isAuthenticated
});

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    clearError: () => dispatch(clearError())
});

const App: React.ComponentClass<Props> =
    connect(mapStateToProps, mapDispatchToProps)(AppComponent);
export default App;