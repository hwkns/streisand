import * as React from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';

import Store from '../store';

export type Props = {};

type ConnectedState = {
    isAuthenticated: boolean;
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
            <div>
                <nav className="navbar navbar-default">
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
                            </ul>
                        </div>
                    </div>
                </nav>
                <div className="container">
                    {this.props.children}
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state: Store.All, props: Props): ConnectedState => ({
    isAuthenticated: state.auth.isAuthenticated
});

const App: React.ComponentClass<Props> =
    connect(mapStateToProps)(AppComponent);
export default App;