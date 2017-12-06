import * as React from 'react';
import { Parser } from 'bbcode-to-react';

const parser = new Parser();

function TextView(props: { content: string }) {
    return (
        <div style={{ whiteSpace: 'pre-wrap' }}>{parser.toReact(props.content)}</div>
    );
}

export default TextView;