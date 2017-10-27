import { RouterState } from 'react-router-redux';

import IFilm from '../models/IFilm';
import IAuthInfo from '../models/IAuthInfo';
import ILocationInfo from '../models/ILocationInfo';
import IPagedItemSet from '../models/base/IPagedItemSet';

namespace Store {
    export type Films = IPagedItemSet<IFilm>;

    export type All = {
        routing: RouterState;
        location: ILocationInfo;
        auth: IAuthInfo;
        films: Films;
    };
}

export default Store;
