import * as React from 'react';

export interface ITextEditorHandle {
    getContent: () => string;
}

export type Props = {
    content: string;
    startingHeight: number;
    receiveHandle?: (handle: ITextEditorHandle) => void;
};

type State = {
    content: string;
};

export default class TextEditor extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);

        this.state = {
            content: ''
        };
    }

    public componentWillMount() {
        this.setState({ content: this.props.content });
    }

    public componentDidMount() {
        if (this.props.receiveHandle) {
            this.props.receiveHandle({
                getContent: () => { return this.state.content; }
            });
        }
    }

    public componentWillReceiveProps(props: Props) {
        this.setState({ content: props.content });
    }

    public render() {
        return <textarea
            className="form-control"
            style={{ height: `${this.props.startingHeight}px`}}
            spellCheck={true}
            value={this.state.content}
            onChange={this._handleChange.bind(this)}
        />;
    }

    private _handleChange(event: React.ChangeEvent<HTMLTextAreaElement>) {
        this.setState({ content: event.target.value });
    }
}