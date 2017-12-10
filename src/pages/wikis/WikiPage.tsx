import * as React from 'react';
import * as redux from 'redux';
import { connect } from 'react-redux';

import Store from '../../store';
import IWiki from '../../models/IWiki';
import Empty from '../../components/Empty';
import WikiView from '../../components/wikis/WikiView';
import { numericIdentifier } from '../../utilities/shim';
import { getWiki } from '../../actions/wikis/WikiAction';
import ILoadingItem from '../../models/base/ILoadingItem';

export type Props = {
    params: {
        wikiId: string;
    };
};

type ConnectedState = {
    wikiId: number;
    wiki: IWiki;
    loading: boolean;
};

type ConnectedDispatch = {
    getWiki: (id: number) => void;
};

type CombinedProps = ConnectedState & ConnectedDispatch & Props;
class WikiPageComponent extends React.Component<CombinedProps, void> {
    public componentWillMount() {
        if (!this.props.loading && !this.props.wiki) {
            this.props.getWiki(this.props.wikiId);
        }
    }

    public componentWillReceiveProps(props: CombinedProps) {
        if (!props.loading && !props.wiki) {
            this.props.getWiki(props.wikiId);
        }
    }

    public render() {
        const wiki = this.props.wiki;
        if (this.props.loading || !wiki) {
            return <Empty loading={this.props.loading} />;
        }

        return (
            <WikiView wiki={wiki} />
        );
    }
}

const mapStateToProps = (state: Store.All, ownProps: Props): ConnectedState => {
    console.log('finding wiki');
    const item = state.wikis.byId[ownProps.params.wikiId];
    const loading = (item && (item as ILoadingItem).loading) || false;
    const wiki = (item && typeof (item as IWiki).id !== 'undefined') ? item as IWiki : undefined;

    return {
        loading: loading,
        wiki: wiki,
        wikiId: numericIdentifier(ownProps.params.wikiId)
    };
};

const mapDispatchToProps = (dispatch: redux.Dispatch<Store.All>): ConnectedDispatch => ({
    getWiki: (id: number) => dispatch(getWiki(id))
});

const WikiPage: React.ComponentClass<Props> =
    connect(mapStateToProps, mapDispatchToProps)(WikiPageComponent);
export default WikiPage;
