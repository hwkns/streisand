import * as React from 'react';
import { Parser } from 'bbcode-to-react';

import IWiki from '../../models/IWiki';

const parser = new Parser();

export type Props = {
    wiki: IWiki;
};

class WikiView extends React.Component<Props> {
    public render() {
        const wiki = this.props.wiki;
        return (
            <div>
                <h1>{wiki.title}</h1>
                <div>{parser.toReact(wiki.body)}</div>
            </div>
        );
    }
}

export default WikiView;