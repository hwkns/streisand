import AuthAction from './AuthAction';
import FilmAction from './FilmAction';
import TorrentAction from './torrents';
import ErrorAction from './ErrorAction';
import FilmsAction from './FilmsAction';

type Action = ErrorAction | AuthAction | FilmsAction | FilmAction | TorrentAction;
export default Action;
