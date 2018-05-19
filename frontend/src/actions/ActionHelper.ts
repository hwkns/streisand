import Store from '../store';
import { handleError } from './ErrorAction';
import { IUnkownError } from '../models/base/IError';
import { Action, ThunkAction, IDispatch } from './ActionTypes';

export interface ISimpleFetchDataProps<A extends Action, R> {
    errorPrefix: string;
    request: (token: string) => Promise<R>;
    fetching: () => A;
    received: (response: R) => A | ThunkAction<A>;
    failure: () => A;
}

export function simplefetchData<A extends Action, R>(props: ISimpleFetchDataProps<A, R>): ThunkAction<A> {
    return (dispatch: IDispatch<A>, getState: () => Store.All) => {
        const state = getState();
        dispatch(props.fetching());
        return props.request(state.sealed.auth.token).then((response: R) => {
            return dispatch(props.received(response));
        }, (error: IUnkownError) => {
            dispatch(handleError(error, props.errorPrefix));
            return dispatch(props.failure());
        });
    };
}

export interface IFetchDataProps<A extends Action, P, R> {
    props: P;
    errorPrefix: string;
    request: (token: string, params: P) => Promise<R>;
    fetching: (params: P) => A;
    received: (params: P, response: R) => A | ThunkAction<A>;
    failure: (params: P) => A;
}

export function fetchData<A extends Action, P, R>(props: IFetchDataProps<A, P, R>): ThunkAction<A> {
    return (dispatch: IDispatch<A>, getState: () => Store.All) => {
        const state = getState();
        dispatch(props.fetching(props.props));
        return props.request(state.sealed.auth.token, props.props).then((response: R) => {
            return dispatch(props.received(props.props, response));
        }, (error: IUnkownError) => {
            dispatch(handleError(error, props.errorPrefix));
            return dispatch(props.failure(props.props));
        });
    };
}