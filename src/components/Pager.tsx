import * as React from 'react';
import { Link } from 'react-router';

import globals from '../utilities/globals';

const PAGE_SIZE = globals.pageSize;
const MAX_PAGES = 10;

export type Props = {
    page: number;
    total: number;
};

const center = {
    'display': 'flex',
    'justify-content': 'center'
};

function Pager(props: Props) {
    let pages = [];
    const half = MAX_PAGES / 2;
    const pageCount = Math.ceil(props.total / PAGE_SIZE);
    let left = props.page - half > 0 ? props.page - half : props.page - props.page - 1;
    let right = Math.min(pageCount, props.page + MAX_PAGES - (props.page - left));
    left = Math.max(1, props.page - MAX_PAGES + (right - props.page));
    for (let i = left; i <= right; i++) {
        const start = PAGE_SIZE * (i - 1) + 1;
        const end = Math.min(start + PAGE_SIZE - 1, props.total);
        const classes = i === props.page ? 'active' : '';
        pages.push(<li className={classes} key={i} title={`${start} - ${end}`}><Link to={`/films/${i}`}>{i}</Link></li>);
    }
    return (
        <ul style={center} className="pagination">
            <li className={props.page === 1 ? 'disabled' : ''}>
                <Link to="/films/1">«</Link>
            </li>
            {pages}
            <li className={props.page === pageCount ? 'disabled' : ''}>
                <Link to={`/films/${pageCount}`}>» </Link>
            </li>
        </ul>
    );
}

export default Pager;