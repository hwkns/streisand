import * as React from 'react';
import * as redux from 'redux';
import { connect } from 'react-redux';

import Store from '../../store';
import IWiki, { IWikiUpdate } from '../../models/IWiki';
import TextView from '../bbcode/TextView';
import TextEditor, { ITextEditorHandle } from '../bbcode/TextEditor';
import WikiCommandBar from './WikiCommandBar';
import { updateWiki } from '../../actions/wikis/WikiAction';

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
    private _editorHandle: ITextEditorHandle;

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
            // A rough estimate of how much space is available on the page
            // with a minimum starting height of 250 px
            const height = Math.max(250, window.innerHeight - 220);
            const onHandle = (handle: ITextEditorHandle) => { this._editorHandle = handle; };
            return (
                <div>
                    <WikiCommandBar wiki={wiki} editMode={editMode} operations={operations} />
                    <h1>{wiki.title}</h1>
                    <TextEditor content={wiki.body} receiveHandle={onHandle} startingHeight={height} />
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