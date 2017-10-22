import { RouterState } from 'react-router-redux';

import IFilm from '../models/IFilm';
import IAuthInfo from '../models/IAuthInfo';
import ILocationInfo from '../models/ILocationInfo';

type BasicItemSet<T> = {
    byId: { [id: string]: T };
    allIds: string[]
};

type LoadingItemSet<T> = BasicItemSet<T> & {
    loading: boolean;
};

namespace Store {
    export type Films = LoadingItemSet<IFilm>;

    export type All = {
        routing: RouterState;
        location: ILocationInfo;
        auth: IAuthInfo;
        films: Films;
    };
}

export default Store;
