import WikiAction from './WikiAction';
import WikisAction from './WikisAction';
import CreateWikiAction from './CreateWikiAction';

type Action = WikisAction | CreateWikiAction | WikiAction;
export default Action;