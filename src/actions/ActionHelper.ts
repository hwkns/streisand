import Store from '../store';
import { handleError } from './ErrorAction';
import { IUnkownError } from '../models/base/IError';
import { ReduxAction, ThunkAction, IDispatch } from './ActionTypes';

export interface IFetchProps<A extends ReduxAction, P, R> {
    props?: P;
    errorPrefix?: string;
    fetch: (token: string, params?: P) => Promise<R>;
    fetching: (params?: P) => A;
    received: (response: R) => A;
    failure: (params?: P) => A;
}

export function fetchData<A extends ReduxAction, P, R>(props: IFetchProps<A, P, R>): ThunkAction<A> {
    return (dispatch: IDispatch<A>, getState: () => Store.All) => {
        const state = getState();
        dispatch(props.fetching(props.props));
        return props.fetch(state.sealed.auth.token, props.props).then((response: R) => {
            return dispatch(props.received(response));
        }, (error: IUnkownError) => {
            dispatch(handleError(error, props.errorPrefix));
            return dispatch(props.failure(props.props));
        });
    };
}