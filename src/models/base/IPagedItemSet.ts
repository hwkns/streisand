import ILoadingItem from './ILoadingItem';

export interface IPage<T> {
    loading: boolean;
    items: T[];
}

export interface IPagedItemSet<T> {
    count: number;
    byId: { [id: number]: ILoadingItem | T };
    pages: { [page: number]: IPage<T> };
}

export default IPagedItemSet;