import WikiAction from './wikis';
import FilmAction from './films';
import AuthAction from './AuthAction';
import TorrentAction from './torrents';
import ErrorAction from './ErrorAction';
import DeviceAction from './DeviceAction';

type Action = ErrorAction
    | AuthAction
    | FilmAction
    | TorrentAction
    | DeviceAction
    | WikiAction;
export default Action;
