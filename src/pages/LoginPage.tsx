import * as React from 'react';
import * as redux from 'redux';
import { connect } from 'react-redux';

import Store from '../store';
import { login } from '../actions/AuthAction';

export type Props = {};
type ConnectedDispatch = {
    login: (username: string, password: string) => void;
};

type State = {
    username: string;
    password: string;
};

type CombinedProps = Props & ConnectedDispatch;
class LoginComponent extends React.Component<CombinedProps, State> {
    constructor() {
        super();

        this.state = {
            username: '',
            password: ''
        };
    }

    public handleUserNameChange(event: React.ChangeEvent<HTMLInputElement>) {
        this.setState({
            username: event.target.value,
            password: this.state.password
        });
    }

    public handlePasswordChange(event: React.ChangeEvent<HTMLInputElement>) {
        this.setState({
            username: this.state.username,
            password: event.target.value
        });
    }

    public render() {
        const { login } = this.props;
        return (
            <div>
                <div className="well bs-component">
                    <form className="form-horizontal">
                        <fieldset>
                            <legend>Sign in</legend>
                            <div className="form-group">
                                <label htmlFor="inputEmail" className="col-lg-2 control-label">Email</label>
                                <div className="col-lg-10">
                                    <input type="text" className="form-control" id="inputEmail" placeholder="Email"
                                        value={this.state.username} onChange={(event) => this.handleUserNameChange(event)} />
                                </div>
                            </div>
                            <div className="form-group">
                                <label htmlFor="inputPassword" className="col-lg-2 control-label">Password</label>
                                <div className="col-lg-10">
                                    <input type="password" className="form-control" id="inputPassword" placeholder="Password"
                                        value={this.state.password} onChange={(event) => this.handlePasswordChange(event)} />
                                </div>
                            </div>
                        </fieldset>
                    </form>
                    <div>
                        <button className="btn btn-primary" onClick={() => login(this.state.username, this.state.password)}>Login</button>
                    </div>
                </div>
            </div>
        );
    }
}

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    login: (username: string, password: string) => dispatch(login(username, password))
});

const LoginPage: React.ComponentClass<Props> =
    connect(undefined, mapDispatchToProps)(LoginComponent);
export default LoginPage;
