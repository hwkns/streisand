import * as React from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';

import Store from '../store';

export type Props = {};

type ConnectedState = {
    isAuthenticated: boolean;
    authError: string;
    errorMessage: string;
};

type CombinedProps = Props & ConnectedState;
class AppComponent extends React.Component<CombinedProps> {
    public render() {
        const links = !this.props.isAuthenticated ? undefined : (
            <ul className="nav navbar-nav">
                <li><Link to="/films">Films</Link></li>
            </ul>
        );
        return (
            <div style={{'paddingTop': '80px'}}>
                <nav className="navbar navbar-default navbar-fixed-top">
                    <div className="container">
                        <div className="navbar-header">
                            <Link className="navbar-brand" to="/">JumpCut</Link>
                            <button className="navbar-toggle collapsed" type="button" data-toggle="collapse" data-target="#navbar-main">
                                <span className="icon-bar"></span>
                                <span className="icon-bar"></span>
                                <span className="icon-bar"></span>
                            </button>
                        </div>
                        <div className="navbar-collapse collapse" id="navbar-main">
                            {links}
                            <ul className="nav navbar-nav navbar-right">
                                <li><Link to="/about">About</Link></li>
                                <li className="dropdown">
                                    <a className="dropdown-toggle" data-toggle="dropdown" href="#" id="themes" aria-expanded="false">Settings <span className="caret"></span></a>
                                    <ul className="dropdown-menu" aria-labelledby="themes">
                                        <li><Link to="/themes">Themes</Link></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                    </div>
                </nav>
                <div className="container">
                    {this._getErrorBanner()}
                    {this.props.children}
                </div>
            </div>
        );
    }

    private _getErrorBanner() {
        const message = this.props.authError || this.props.errorMessage;
        return !message ? undefined : (
            <div className="bs-component">
                <div className="alert alert-dismissible alert-danger">
                    <button type="button" className="close" data-dismiss="alert">×</button>
                    {message}
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state: Store.All, props: Props): ConnectedState => ({
    errorMessage: state.errors.unkownError,
    authError: state.errors.authError,
    isAuthenticated: state.auth.isAuthenticated
});

const App: React.ComponentClass<Props> =
    connect(mapStateToProps)(AppComponent);
export default App;