import AuthAction from './AuthAction';
import FilmAction from './FilmAction';
import ErrorAction from './ErrorAction';
import FilmsAction from './FilmsAction';
import TorrentAction from './TorrentAction';
import TorrentsAction from './TorrentsAction';

type Action = ErrorAction | AuthAction | FilmsAction | FilmAction | TorrentsAction | TorrentAction;
export default Action;
