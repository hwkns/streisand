import * as React from 'react';
import { Parser } from 'bbcode-to-react';

const parser = new Parser();
const style: React.CSSProperties = {
    whiteSpace: 'pre-wrap',
    wordBreak: 'break-word'
};

function TextView(props: { content: string }) {
    return (
        <div style={style}>{parser.toReact(props.content)}</div>
    );
}

export default TextView;