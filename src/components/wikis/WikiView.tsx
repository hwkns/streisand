import * as React from 'react';
import * as redux from 'redux';
import { connect } from 'react-redux';

import Store from '../../store';
import TextView from '../bbcode/TextView';
import WikiCommandBar from './WikiCommandBar';
import IWiki, { IWikiUpdate } from '../../models/IWiki';
import { updateWiki } from '../../actions/wikis/WikiAction';
import Editor, { IEditorHandle } from '../bbcode/Editor';

export type Props = {
    wiki: IWiki;
};

type State = {
    editMode: boolean;
};

type ConnectedState = {};

type ConnectedDispatch = {
    updateWiki: (id: number, wiki: IWikiUpdate) => void;
};

type CombinedProps = ConnectedState & ConnectedDispatch & Props;
class WikiViewComponent extends React.Component<CombinedProps, State> {
    private _editorHandle: IEditorHandle;

    constructor(props: CombinedProps) {
        super(props);

        this.state = {
            editMode: false
        };
    }

    public render() {
        const wiki = this.props.wiki;
        const editMode = this.state.editMode;
        const operations = {
            onEdit: () => { this.setState({ editMode: true }); },
            onCancel: () => { this.setState({ editMode: false }); },
            onSave: () => {
                this.props.updateWiki(wiki.id, {
                    title: wiki.title,
                    body: this._editorHandle.getContent()
                });
            }
        };

        if (editMode) {
            const onHandle = (handle: IEditorHandle) => { this._editorHandle = handle; };
            return (
                <div>
                    <WikiCommandBar wiki={wiki} editMode={editMode} operations={operations} />
                    <h1>{wiki.title}</h1>
                    <Editor content={wiki.body} receiveHandle={onHandle} size="large" />
                </div>
            );
        }

        return (
            <div>
                <WikiCommandBar wiki={wiki} editMode={editMode} operations={operations} />
                <h1>{wiki.title}</h1>
                <TextView content={wiki.body} />
            </div>
        );
    }
}

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    updateWiki: (id: number, wiki: IWikiUpdate) => dispatch(updateWiki(id, wiki))
});

const WikiView: React.ComponentClass<Props> =
    connect(undefined, mapDispatchToProps)(WikiViewComponent);
export default WikiView;