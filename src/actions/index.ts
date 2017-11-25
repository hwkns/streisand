import AuthAction from './AuthAction';
import FilmAction from './FilmAction';
import TorrentAction from './torrents';
import ErrorAction from './ErrorAction';
import FilmsAction from './FilmsAction';
import DeviceAction from './DeviceAction';

type Action = ErrorAction
    | AuthAction
    | FilmsAction
    | FilmAction
    | TorrentAction
    | DeviceAction;
export default Action;
