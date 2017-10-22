import Store from '../store';

export type ReduxAction = { type: string; };
export type ThunkAction<T extends ReduxAction> = (dispatch: IDispatch<T>, getState: () => Store.All) => T | ThunkAction<T> | Promise<ReduxAction | ThunkAction<T>>;
export interface IDispatch<T extends ReduxAction> {
    (action: T | ThunkAction<T>): T;
}