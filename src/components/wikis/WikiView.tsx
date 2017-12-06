import * as React from 'react';

import IWiki from '../../models/IWiki';
import TextView from '../bbcode/TextView';

export type Props = {
    wiki: IWiki;
};

class WikiView extends React.Component<Props> {
    public render() {
        const wiki = this.props.wiki;
        return (
            <div>
                <h1>{wiki.title}</h1>
                <TextView content={wiki.body} />
            </div>
        );
    }
}

export default WikiView;