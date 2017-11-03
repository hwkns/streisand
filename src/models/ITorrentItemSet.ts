import ITorrent from './ITorrent';
import { IPagedItemSet, IPage } from './base/IPagedItemSet';

interface ITorrentItemSet extends IPagedItemSet<ITorrent> {
    byFilmId: { [id: string]: IPage<ITorrent> };
}

export default ITorrentItemSet;