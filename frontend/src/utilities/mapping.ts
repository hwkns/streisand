import IItemNode from '../models/base/IItemNode';
import { defaultStatus } from '../models/base/ILoadingStatus';
import { IPage, INodeMap } from '../models/base/IPagedItemSet';

export interface IGetItemsProps<T> {
    page: number;
    pages: { [page: number]: IPage };
    byId: INodeMap<T>;
}

/**
 * Returns the list of items for the given page filtering out empty nodes.
 */
export function getItems<T>(props: IGetItemsProps<T>): T[] {
    const page = props.pages[props.page];
    const identifiers = (page ? page.items : []);
    const items: T[] = [];
    for (const id of identifiers) {
        const node = props.byId[id];
        if (node && node.item) {
            items.push(node.item);
        }
    }
    return items;
}

/**
 * Returns the item for the given item assuming the item was loaded.
 */
export interface IGetItemProps<T> {
    id?: number | null;
    byId: INodeMap<T>;
}

export function getItem<T>(props: IGetItemProps<T>): T | undefined {
    const node = props.byId[props.id as number];
    if (node && node.item) {
        return node.item;
    }
}

export function getNode<T>(props: IGetItemProps<T>): IItemNode<T> {
    return props.byId[props.id as number] || { status: defaultStatus };
}