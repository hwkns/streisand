import * as React from 'react';
import * as redux from 'redux';
import { connect } from 'react-redux';

import Store from '../store';
import SiteNav from '../components/SiteNav';
import { ScreenSize } from '../models/IDeviceInfo';
import { clearError } from '../actions/ErrorAction';
import { watchScreenSize } from '../utilities/device';
import Banner, { BannerType } from '../components/Banner';
import { updateScreenSize } from '../actions/DeviceAction';

export type Props = {};

type ConnectedState = {
    authError: string;
    errorMessage: string;
};

type ConnectedDispatch = {
    clearError: () => void;
    updateScreenSize: (screenSize: ScreenSize) => void;
};

type CombinedProps = Props & ConnectedState & ConnectedDispatch;
class AppComponent extends React.Component<CombinedProps> {
    private _screenSizeWatcher: () => void;

    public render() {
        return (
            <div style={{'paddingTop': '80px'}}>
                <SiteNav />
                <div className="container">
                    {this._getErrorBanner()}
                    {this.props.children}
                </div>
            </div>
        );
    }

    public componentWillUnmount() {
        if (this._screenSizeWatcher) {
            window.removeEventListener('resize', this._screenSizeWatcher);
            this._screenSizeWatcher = undefined;
        }
    }

    public componentDidMount() {
        this._screenSizeWatcher = watchScreenSize((screenSize: ScreenSize) => {
            this.props.updateScreenSize(screenSize);
        });
        window.addEventListener('resize', this._screenSizeWatcher);
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
    authError: state.errors.authError
});

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    clearError: () => dispatch(clearError()),
    updateScreenSize: (screenSize: ScreenSize) => dispatch(updateScreenSize(screenSize))
});

const App: React.ComponentClass<Props> =
    connect(mapStateToProps, mapDispatchToProps)(AppComponent);
export default App;