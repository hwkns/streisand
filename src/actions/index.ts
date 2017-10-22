import AuthAction from './AuthAction';
import FilmAction from './FilmAction';
import FilmsAction from './FilmsAction';

type Action = AuthAction | FilmsAction | FilmAction;
export default Action;
