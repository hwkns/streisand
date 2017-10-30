import AuthAction from './AuthAction';
import FilmAction from './FilmAction';
import ErrorAction from './ErrorAction';
import FilmsAction from './FilmsAction';

type Action = ErrorAction | AuthAction | FilmsAction | FilmAction;
export default Action;
