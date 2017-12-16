import { RouterState } from 'react-router-redux';

import IFilm from '../models/IFilm';
import IWiki from '../models/IWiki';
import INewsPost from '../models/INewsPost';
import IAuthInfo from '../models/IAuthInfo';
import IDeviceInfo from '../models/IDeviceInfo';
import ILocationInfo from '../models/ILocationInfo';
import ITorrentItemSet from '../models/ITorrentItemSet';
import IPagedItemSet from '../models/base/IPagedItemSet';

namespace Store {
    export type Films = IPagedItemSet<IFilm>;
    export type Wikis = IPagedItemSet<IWiki>;
    export type News = { latest: INewsPost; loading: boolean; };

    export type Errors = {
        authError: string;
        unkownError: string;
    };

    export type All = {
        errors: Errors;
        routing: RouterState;
        location: ILocationInfo;
        auth: IAuthInfo;
        films: Films;
        torrents: ITorrentItemSet;
        deviceInfo: IDeviceInfo;
        wikis: Wikis;
        news: News;
    };
}

export default Store;
